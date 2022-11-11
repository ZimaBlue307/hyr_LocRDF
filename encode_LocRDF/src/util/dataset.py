from typing import Dict
import pandas as pd


rdfs_p = {
	'type'          : '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>',
	'domain'        : '<http://www.w3.org/2000/01/rdf-schema#domain>',
	'range'         : '<http://www.w3.org/2000/01/rdf-schema#range>',
	'subClassOf'    : '<http://www.w3.org/2000/01/rdf-schema#subClassOf>',
	'subPropertyOf' : '<http://www.w3.org/2000/01/rdf-schema#subPropertyOf>'
}


def read_nt(path) -> pd.DataFrame:
	"""
	读取一个 nt 文件到 DataFrame
	"""
	nt = pd.read_csv(path, delimiter=' ', header=None, names=['s', 'p', 'o', '.']).astype(str).iloc[:, :3]
	return nt


def nt2idx(nt : pd.DataFrame) -> Dict[str, pd.DataFrame]:
	"""
	将 DataFrame 中, 根据 p 的类型, 做 idx 索引, 以及字面量索引
	"""
	type_idx = nt[nt['p'] == rdfs_p['type']]
	domain_idx = nt[nt['p'] == rdfs_p['domain']]
	range_idx = nt[nt['p'] == rdfs_p['range']]
	subClassOf_idx = nt[nt['p'] == rdfs_p['subClassOf']]
	subPropertyOf_idx = nt[nt['p'] == rdfs_p['subPropertyOf']]
	normal_p = nt
	literal_idx = nt[nt['o'].str.startswith('<') == False]
	idx: Dict[str, pd.DataFrame] = {
		'type'          : type_idx,
		'domain'        : domain_idx,
		'range'         : range_idx,
		'subClassOf'    : subClassOf_idx,
		'subPropertyOf' : subPropertyOf_idx,
		"normal_p"		: normal_p,
		"literal_idx"	: literal_idx
	}
	return idx
