from typing import List, Dict
import time
from tqdm import tqdm
import numpy as np
import pandas as pd

from tree import TreeNode
from util.single_instance import P2DR, P2DomainRange, U2E, Uri2Encode

class Encode():
	def __init__(self, nt: pd.DataFrame, idx: Dict[str, pd.DataFrame], tree_root: TreeNode, class_or_property: str) -> None:
		self.nt = nt
		self.idx = idx

		self.tree_root_ = tree_root

		self.dataset_root_ = []
		self.class_or_property_ = class_or_property
		if class_or_property == 'Class':
			self.dataset_root_ = [
				'<http://www.w3.org/2000/01/rdf-schema#Class>',
				'<http://www.w3.org/2002/07/owl#Class>'
			]
		elif class_or_property == 'Property':
			self.dataset_root_ = [
				'<http://www.w3.org/1999/02/22-rdf-syntax-ns#Property>',
				'<http://www.w3.org/2002/07/owl#OntologyProperty>',
				'<http://www.w3.org/2002/07/owl#TransitiveProperty>',
				'<http://www.w3.org/2002/07/owl#DatatypeProperty>',
				'<http://www.w3.org/2002/07/owl#ObjectProperty>',
				'<http://www.w3.org/2002/07/owl#AnnotationProperty>'
			]


	def find_root(self) -> list:
		""" 找到 class 或 property 的根类 """
		roots = []
		for i in range(len(self.idx['type'])):
			if self.idx['type'].iloc[i]['o'] in self.dataset_root_:
				roots.append(self.idx['type'].iloc[i]['s'])

		for i in range(len(self.idx[f'sub{self.class_or_property_}Of'])):		# 'subPropertyOf' or 'subClassOf'
			if self.idx[f'sub{self.class_or_property_}Of'].iloc[i]['s'] in roots:
				roots.remove(self.idx[f'sub{self.class_or_property_}Of'].iloc[i]['s'])

		for root in roots:
			self.tree_root_.childs_.append(TreeNode(root))


	def find_child(self, parent: TreeNode) -> list:
		for i in range(len(self.idx[f'sub{self.class_or_property_}Of'])):
			if (self.idx[f'sub{self.class_or_property_}Of'].iloc[i]['o'] == parent.val_):
				parent.childs_.append(TreeNode(self.idx[f'sub{self.class_or_property_}Of'].iloc[i]['s']))


	def dfs(self, stack: List[TreeNode]):
		while (len(stack) != 0):
			parent = stack.pop()
			self.find_child(parent)
			stack += parent.childs_

	def run(self):
		self.find_root()
		self.dfs(self.tree_root_.childs_.copy())


class EncodeInstance():
	def __init__(self, rdf_nt: pd.DataFrame, rdf_idx: Dict[str, pd.DataFrame], nt: pd.DataFrame, idx: Dict[str, pd.DataFrame]) -> None:
		self.rdf_nt = rdf_nt
		self.rdf_idx = rdf_idx
		self.nt = nt
		self.idx = idx


	def instance_encode(self):
		"""
		对所有的instance编码
		"""
		p2dr = P2DomainRange(self.rdf_nt, self.rdf_idx)
		uri2encode = Uri2Encode()

		start = time.time()
		print('处理所有 type', end='')
		def type2encode(s: str, p: str, o: str):
			if o in uri2encode.class_:
				uri2encode.class_instance[s] = uri2encode.class_[o]
			else:
				print("type 语句中, o 不存在", s, p, o)
		self.idx['type'].apply(lambda row: type2encode(row['s'], row['p'], row['o']), axis=1)
		print("type 语句处理完毕, 耗时:", time.time() - start)

		# 处理所有 literal
		start = time.time()
		print('处理所有 literal', end='')
		def literal2encode(s: str, p: str, o: str):
			uri2encode.class_instance[o] = uri2encode.class_['literal']
		self.idx['literal_idx'].apply(lambda row: literal2encode(row['s'], row['p'], row['o']), axis=1)
		print("literal 语句处理完毕, 耗时:", time.time() - start)

		# 处理所有 normal_p, 此时要使用 domain 和 range 推理, 并给没有编码的实例编码
		start = time.time()
		print('domain range 推理', end='')
		def dp2encode(s: str, p: str, o: str):
			if s not in uri2encode.class_:
				if p2dr(p, 'domain') != '':
					if s not in uri2encode.class_instance:
						uri2encode.class_instance[s] = uri2encode.class_[p2dr(p, 'domain')]
					else:
						domain_type = uri2encode.class_[p2dr(p, 'domain')]
						type_type = uri2encode.class_instance[s]
						# domain_type 是 type_type 的子类
						if (type_type.pre < domain_type.pre) and (domain_type.post < type_type.post):
							uri2encode.class_instance[s] = domain_type
							print(f"p: {p}")
							print(f"domain [{p2dr(p, 'domain')} \t s_type [{s}]]")
							print(f"type_type [{type_type.pre} \t {type_type.post}]")
							print(f"domain_type [{domain_type.pre} \t {domain_type.post}]")
				else:
					if s not in uri2encode.class_instance:
						uri2encode.class_instance[s] = uri2encode.class_['notype']
			if o not in uri2encode.class_:
				if p2dr(p, 'range') != '':
					if o not in uri2encode.class_instance:
						uri2encode.class_instance[o] = uri2encode.class_[p2dr(p, 'range')]
					else:
						range_type = uri2encode.class_[p2dr(p, 'range')]
						type_type = uri2encode.class_instance[o]
						# range_type 是 type_type 的子类
						if (type_type.pre < domain_type.pre) and (domain_type.post < type_type.post):
							uri2encode.class_instance[o] = range_type
				else:
					if o not in uri2encode.class_instance:
						uri2encode.class_instance[o] = uri2encode.class_['notype']
		self.idx['normal_p'].apply(lambda row: dp2encode(row['s'], row['p'], row['o']), axis=1)
		print(f'\r处理所有 normal_p 用时 {time.time() - start}')
