from typing import Dict
import pandas as pd


class P2DR:
	"""
	单个 p 的 domain 和 range, 如果不存在, 则返回空字符串
	"""
	def __init__(self, domain='', range='') -> None:
		self.domain = domain
		self.range = range

class P2DomainRange:
	"""
	p 的 domain 和 range 表
	"""
	instance = None
	flag = False

	def __new__(cls, nt: pd.DataFrame, idx: Dict[str, pd.DataFrame]):
		if cls.instance is None:
			cls.instance = super(P2DomainRange, cls).__new__(cls)
		return cls.instance

	def __init__(self, nt: pd.DataFrame, idx: Dict[str, pd.DataFrame]) -> None:
		if not P2DomainRange.flag:
			self.p2dr: Dict[str, P2DR] = {}
			self.nt = nt
			self.idx = idx
			for i in range(len(self.idx['domain'])):
				s, p, o = self.idx['domain'].iloc[i]['s'], self.idx['domain'].iloc[i]['p'], self.idx['domain'].iloc[i]['o']
				if s not in self.p2dr:
					self.p2dr[s] = P2DR()
				self.p2dr[s].domain = o
			for i in range(len(self.idx['range'])):
				s, p, o = self.idx['range'].iloc[i]['s'], self.idx['range'].iloc[i]['p'], self.idx['range'].iloc[i]['o']
				if s not in self.p2dr:
					self.p2dr[s] = P2DR()
				self.p2dr[s].range = o
			P2DomainRange.flag = True

	def __call__(self, p: str, domain_or_range: str) -> str:
		"""
		返回 p 的 domain 或 range, 如果不存在, 则返回空字符串
		"""
		assert domain_or_range in ['domain', 'range']

		if p not in self.p2dr:
			return ''

		if domain_or_range == 'domain':
			return self.p2dr[p].domain
		else:
			return self.p2dr[p].range


class U2E:
	"""
	单个 uri 的 encode
	"""
	def __init__(self) -> None:
		self.pre: int = None
		self.post: int = None

class Uri2Encode:
	instance = None
	flag = False

	def __new__(cls, *args, **kwargs):
		if cls.instance is None:
			cls.instance = super(Uri2Encode, cls).__new__(cls)
		return cls.instance

	def __init__(self) -> None:
		if not Uri2Encode.flag:
			self.class_: Dict[str, U2E] = {}
			self.property: Dict[str, U2E] = {}
			self.class_instance: Dict[str, U2E] = {}
			Uri2Encode.flag = True