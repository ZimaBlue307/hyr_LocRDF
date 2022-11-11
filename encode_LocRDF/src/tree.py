from typing import Dict, List

import numpy as np
import pandas as pd

from util.single_instance import U2E, Uri2Encode

class TreeNode:

	def __init__(self, val: str) -> None:
		self.val_ = val
		self.childs_: List[TreeNode] = []


	def pre_order(self, str2encode: Dict[str, U2E], tmp: list):
		if self.val_ not in str2encode:
			str2encode[self.val_] = U2E()
		str2encode[self.val_].pre = len(tmp)
		tmp.append(self)
		for child in self.childs_:
			child.pre_order(str2encode, tmp)


	def post_order(self, str2encode: Dict[str, U2E], tmp: list):
		for child in self.childs_:
			child.post_order(str2encode, tmp)
		str2encode[self.val_].post = len(tmp)
		tmp.append(self)


	def pre_and_post_order(self, str2encode: Dict[str, U2E]):
		tmp = []
		self.pre_order(str2encode, tmp)
		self.post_order(str2encode, tmp)
