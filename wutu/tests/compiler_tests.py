import unittest
from wutu.util import load_module
from test_util import *
from wutu.compiler import *

class CompilerTests(unittest.TestCase):
    def test_initial_tmpl(self):
        result = create_base()
        expected = """var wutu = angular.module("wutu", []);"""
        self.assertEqual(result.strip(), expected)

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
        result = add_variable(stream, "test", "hello")
        excepted = "var test = \"hello\";"
        self.assertEqual(excepted, result)

    def test_int_argument(self):
        stream = create_stream()
        result = add_variable(stream, "test", 123)
        excepted = "var test = 123;"
        self.assertEqual(excepted, result)

