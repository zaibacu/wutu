import unittest
from wutu.util import *
import os


def test_locator(*dir):
	return os.path.join(os.path.dirname(os.path.realpath(__file__)), *dir)

class UtilTests(unittest.TestCase):
	def test_directory_scan(self):
		modules = get_modules(test_locator)
		self.assertEqual(modules, ["test_module"])

	def test_module_injector(self):
		@inject_module("test_module", test_locator)
		def injected_fn(module):
			self.assertEqual(module.ping(), "pong")

		injected_fn()
