from typing import List, Dict


class Entity:
	def __init__(self, id='', class_id=''):
		self.id = id
		self.type = "notype"
		self.attribute = {'type_': class_id}


class EntityTable:
	def __init__(self, name=""):
		self.name = name
		self.id2entity: Dict[str, Entity] = {}
		self.attribute: List[str] = ['type_']


class Edge:
	def __init__(self, start_id="", end_id=""):
		self.start_id = start_id
		self.end_id = end_id
		self.type = "notype"
		self.attribute = {}


class EdgeTable:
	def __init__(self, name=""):
		self.name = name
		self.edgeList: List[Edge] = []
