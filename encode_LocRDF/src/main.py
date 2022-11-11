import os
from typing import List, Dict
from tqdm import tqdm
import time

import numpy as np
import pandas as pd

from params import get_params
from util.format.change import get_nt_files
from util.dataset import read_nt, nt2idx
from util.single_instance import P2DR, P2DomainRange, U2E, Uri2Encode
from tree import TreeNode
from encode import Encode, EncodeInstance
from nt2csv import Entity, EntityTable, Edge, EdgeTable
from util.create_yaml import FileYaml, CreateYaml


log = True
param = get_params()
DILIMITER = ','
if __name__ == '__main__':
	""" 读取数据集 """
	rdf = read_nt('../data/rdfs/rdf.nt')
	rdfs = read_nt('../data/rdfs/rdfs.nt')
	owl = read_nt('../data/rdfs/owl.nt')
	univ_bench = read_nt('../data/rdfs/univ-bench.nt')

	normal_nt = pd.concat([rdf, rdfs, owl, univ_bench], axis=0)
	idx = nt2idx(normal_nt)

	""" 构建树 """
	# 数据集总 root
	class_tree = TreeNode('dataset')
	class_tree.childs_.append(TreeNode('notype'))     	# 处理没有类的实例
	class_tree.childs_.append(TreeNode('literal'))		# 处理 literal
	property_tree = TreeNode('dataset')

	# 找到 root 类 和 root 属性
	class_encode = Encode(normal_nt, idx, class_tree, 'Class')
	property_encode = Encode(normal_nt, idx, property_tree, 'Property')

	class_encode.run()
	property_encode.run()

	""" 前序后序遍历得到编码, 存在 uri2encode 中 """
	uri2encode = Uri2Encode()
	uri2id = {}
	class_tree.pre_and_post_order(uri2encode.class_)
	property_tree.pre_and_post_order(uri2encode.property)

	""" 存储编码 以及 建立 id2entity_table 和 id2edge_table 准备转 csv """
	id2entity_table: Dict[str, EntityTable] = {}
	id2edge_table: Dict[str, EdgeTable] = {}

	if not os.path.exists('../encode/'):
		os.mkdir('../encode/')
	with open('../encode/map_class.txt', 'w') as f:
		for uri in uri2encode.class_:
			encode_pre, encode_post = uri2encode.class_[uri].pre, uri2encode.class_[uri].post
			id = f'c_{encode_pre}_{encode_post}_0'
			f.write(f'{id}_{uri}\n')
			# 建立 EntityTable
			id2entity_table[id] = EntityTable(id)
			uri2id[uri] = id
	with open('../encode/map_properties.txt', 'w') as f:
		for uri in uri2encode.property:
			encode_pre, encode_post = uri2encode.property[uri].pre, uri2encode.property[uri].post
			id = f'p_{encode_pre}_{encode_post}_1'
			f.write(f'{id}_{uri}\n')
			# 建立 EdgeTable
			id2edge_table[id] = EdgeTable(id)
			uri2id[uri] = id


	""" ############################## 实例 ################################ """
	print('start 实例编码')
	nt_files = get_nt_files('../data/nt/')
	uxdx_list = []
	for nt_file in nt_files:
		nt = read_nt(nt_file)
		uxdx_list.append(nt)
	uxdxs = pd.concat(uxdx_list, axis=0)
	print('数据集大小:', uxdxs.shape)

	nt_instance = uxdxs
	idx_instance = nt2idx(uxdxs)

	instance_encode = EncodeInstance(normal_nt, idx, uxdxs, idx_instance)
	instance_encode.instance_encode()

	""" 存储 """
	with open('../encode/map_instance_class.txt', 'w') as f:
		for uri in uri2encode.class_instance:
			encode_pre, encode_post = uri2encode.class_instance[uri].pre, uri2encode.class_instance[uri].post
			if (encode_pre == uri2encode.class_['literal'].pre) and (encode_post == uri2encode.class_['literal'].post):
				continue
			class_id = f'c_{encode_pre}_{encode_post}_0'
			id = f'i_{encode_pre}_{encode_post}_{len(id2entity_table[class_id].id2entity)}'
			f.write(f'{id}_{uri}\n')
			# 建立 Entity
			id2entity_table[class_id].id2entity[id] = Entity(id, class_id)
			uri2id[uri] = id


	""" 转换为 csv 以及生成 yaml """
	# 记录将成为 属性的 p
	start_time = time.time()
	print('start 转换为 csv', end='')
	literal_p_list = []
	def nt2csv(s: str, p: str, o: str):
		# 属性
		if p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
			id2entity_table[uri2id[s]].id2entity[uri2id[o]].attribute['type_'] = uri2id[o]
			if 'type_' not in id2entity_table[uri2id[o]].attribute:
				id2entity_table[uri2id[o]].attribute.append('type_')
		# 字面量
		if o[0] != '<':
			uri2classid = lambda uri: f'c_{uri2encode.class_instance[uri].pre}_{uri2encode.class_instance[uri].post}_0'
			if uri2id[p] not in id2entity_table[uri2classid(s)].attribute:
				id2entity_table[uri2classid(s)].attribute.append(uri2id[p])
			id2entity_table[uri2classid(s)].id2entity[uri2id[s]].attribute[uri2id[p]] = o
			literal_p_list.append(uri2id[p])			# 这种 p 不会建egde表
		else:
			new_edge = Edge(uri2id[s], uri2id[o])
			id2edge_table[uri2id[p]].edgeList.append(new_edge)
	nt_instance.apply(lambda row: nt2csv(row['s'], row['p'], row['o']), axis=1)
	print(f'nt2csv 耗时: {time.time() - start_time}')

	if os.path.exists('../csv'):
		os.system(f'rm -rf ../csv')
	os.mkdir('../csv')

	space_name = param.dataset
	yaml_files = []
	sql = [
		f"DROP SPACE IF EXISTS {space_name};",
		f"CREATE SPACE IF NOT EXISTS {space_name}(partition_num=5, replica_factor=1, vid_type=FIXED_STRING(50), use_rdf=1);",
		f"USE {space_name};"
	]

	# 遍历每种class的实例
	for table_id in id2entity_table:
		table = id2entity_table[table_id]
		csv_path = f'../csv/{table.name}.csv'
		# 建立 csv
		csv_content = []
		for entity_id in table.id2entity:
			entity = table.id2entity[entity_id]
			csv_line = entity.id
			for attr in table.attribute:
				if attr in entity.attribute:
					csv_line += f'{DILIMITER}{entity.attribute[attr]}'
				else:
					csv_line += f'{DILIMITER}'
			csv_content.append(csv_line)
		# sql
		attrs = 'type_ string'
		for attr in table.attribute:
			if attr == 'type_':
				continue
			attrs += f', {attr} string'
		create_tag = f"CREATE TAG {table_id}({attrs});"
		sql.append(create_tag)
		# csv文件
		if len(csv_content) == 0:
			continue
		prop_list = []					# yaml
		for attr in table.attribute:
			prop_list.append({"name": attr, "type": "string"})
		yaml_files.append(FileYaml(0, table_id, prop_list))
		with open(csv_path, 'w') as f:	# csv
			for line in csv_content:
				f.write(f'{line}\n')

	# 遍历每种property的实例
	for table_id in id2edge_table:
		if (table_id in literal_p_list):
			continue
		table = id2edge_table[table_id]
		csv_path = f'../csv/{table.name}.csv'
		csv_content = []
		for edge in table.edgeList:
			csv_line = f'{edge.start_id}{DILIMITER}{edge.end_id}'
			csv_content.append(csv_line)
		# sql
		sql.append(f"CREATE EDGE {table_id}();")
		# csv
		if len(csv_content) == 0:
			continue
		yaml_files.append(FileYaml(1, table_id, []))		# yaml
		with open(csv_path, 'w') as f:
			for line in csv_content:
				f.write(f'{line}\n')

	to_yaml = CreateYaml(space_name, yaml_files, sql)
	to_yaml.save('../csv/a_config.yaml')

	# # YAML() 生成的文件对于多行字符串处理的不好看
	# yaml_format = open('../csv/a_config.yaml', 'r+')
	# yaml_content = yaml_format.readlines()
	# yaml_content[13] = '    commands:  |\n'
	# yaml_content[15] = '    - UPDATE CONFIGS storage:rocksdb_column_family_options = { disable_auto_compactions = True };\n'
	# yaml_content[16] = ''
	# yaml_content[18] = f"      CREATE SPACE IF NOT EXISTS {space_name}(partition_num=5, replica_factor=1, vid_type=FIXED_STRING(50), use_rdf=1);\n"
	# yaml_content[19] = ''
	# for i in range(len(yaml_content)):
	# 	if yaml_content[i].find('preStop') != -1:
	# 		break
	# 	yaml_content[i] = yaml_content[i].replace('    - ', '      ')
	# yaml_format = open('../csv/a_config.yaml', 'w+')
	# yaml_format.writelines(yaml_content)

	# 将 encode 文件复制到 nebula 下
	if not os.path.exists('/usr/local/nebula/data/encode'):
		os.makedirs('/usr/local/nebula/data/encode')
	os.system(f'cp ../encode/* /usr/local/nebula/data/encode')
