import unittest
from wutu.util import *
from test_util import *
from wutu.module import module_locator
import os


class UtilTests(unittest.TestCase):
	def setUp(self):
		self.api = ApiMock()

	def test_directory_scan(self):
		modules = get_modules(test_locator)
		self.assertEqual(modules, ["test_module"])

	def test_module_injector(self):
		@inject_module("test_module", test_locator)
		def injected_fn(module):
			self.assertEqual(module.ping(), "pong")

		injected_fn()

	def test_module_locator(self):
		module = load_module(get_modules(test_locator)[0])
		result = module_locator(module, "controller.js")
		expected = "{0}/modules/test_module/controller.js".format(os.getcwd())
		compare_dir(self.assertEqual, expected, result)

