import unittest
from wutu.test_util import *
from wutu.module import module_locator, Module
from wutu.decorators import *


class UtilTests(unittest.TestCase):
	def setUp(self):
		self.api = ApiMock()

	def test_directory_scan(self):
		modules = load_modules(test_locator)
		self.assertEqual(modules, ["test_module"])

	def test_module_injector(self):
		@inject_module("test_module")
		def injected_fn(module):
			self.assertEqual(module.ping(), "pong")

		injected_fn()

	def test_module_locator(self):
		module = load_module(load_modules()[0])
		result = module_locator(module, "controller.js")
		expected = "modules/test_module/controller.js"
		self.assertEqual(expected, result.replace("\\", "/"))

	def test_endpoint_name(self):
		result = endpoint_name("TestModule")
		expected = "test_module"
		compare_dir(self.assertEqual, expected, result)

	def test_module_creator(self):
		@create_module(self.api)
		def new_module():
			return {"get": lambda req: "Hello, world!"}

		self.assertEqual("Hello, world!", self.api.call("/new_module", "get"))

	def test_module_identity(self):
		module = load_module(load_modules()[0])
		result = get_identity(module)
		expected = ["_id"]
		self.assertEqual(expected, result)
