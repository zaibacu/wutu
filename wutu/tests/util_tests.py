import unittest
from wutu.util import *

class UtilTests(unittest.TestCase):
	def test_directory_scan(self):
		modules = get_modules()
		print(modules)
		self.assertEqual(modules, ["test_module"])