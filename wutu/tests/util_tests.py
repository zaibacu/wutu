import unittest
from wutu.util import *
from wutu.tests.util import *


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
