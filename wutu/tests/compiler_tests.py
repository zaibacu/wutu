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
        print(result)
        expected = """
            function(test1, test2){
                console.log('Hello world!');
            }
        """
        compare(self.assertEqual, result.strip(), expected.strip())