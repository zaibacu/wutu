import unittest
from wutu.util import *
import os

class ApiMock(object):
	def add_resource(self, res, *args):
		pass

def test_locator(*dir):
	return os.path.join(os.path.dirname(os.path.realpath(__file__)), *dir)

class UtilTests(unittest.TestCase):
	def setUp(self):
		self.api = ApiMock()

	def test_directory_scan(self):
		modules = get_modules(test_locator)
		self.assertEqual(modules, ["test_module"])

	def test_module_injector(self):
		@inject_module(self.api, "test_module", test_locator)
		def injected_fn(module):
			self.assertEqual(module.ping(), "pong")

		injected_fn()
