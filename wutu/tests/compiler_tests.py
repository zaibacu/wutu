import unittest
from test_util import *
from compiler import *
from util import *


class CompilerTests(unittest.TestCase):
	def test_initial_tmpl(self):
		stream = create_stream()
		create_base(stream)
		result = get_data(stream)
		expected = """
				var base_url = function(){ return "/"; };
				var wutu = angular.module("wutu", []);
			"""
		compare(self.assertEqual, expected.strip(), result.strip())

	def test_function_block(self):
		stream = create_stream()
		with function_block(stream, ["test1", "test2"]) as block:
			block.write("console.log('Hello world!');")

		result = get_data(stream)
		expected = """
			function(test1, test2){
				console.log('Hello world!');
			}
		"""
		compare(self.assertEqual, expected.strip(), result.strip())

	def test_service_block(self):
		stream = create_stream()
		with service_block(stream) as service:
			service.add_method("test_fn", ["test1", "test2"], lambda s: s.write("return true;"))
			service.add_method("test_fn2", ["test3"], lambda s: s.write("return false;"))

		result = get_data(stream)
		print(result)
		expected = """
			var service = {
			 test_fn: function(test1, test2){
				return true;
			 },
			 test_fn2: function(test3){
				return false;
			 }
			}
			return service;
		"""
		compare(self.assertEqual, expected.strip(), result.strip())

	def test_string_argument(self):
		stream = create_stream()
		add_variable(stream, "test", "hello")
		result = get_data(stream).strip()
		excepted = "var test = \"hello\";"
		self.assertEqual(excepted, result)

	def test_int_argument(self):
		stream = create_stream()
		add_variable(stream, "test", 123)
		result = get_data(stream).strip()
		excepted = "var test = 123;"
		self.assertEqual(excepted, result)

	def test_module(self):
		mod = Module()
		mod.__name__ = "test_module"
		stream = StringIO()
		create_base(stream)
		mod.create_service(stream)
		self.assertTrue(validate_js(get_data(stream)))

