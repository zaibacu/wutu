import unittest
from wutu.util import load_module
from test_util import *
from wutu.compiler import *

class CompilerTests(unittest.TestCase):
    def test_service_tmpl(self):
        mod = load_module("test_module", test_locator)
        result = create_service_js(mod)
        print(result)
        self.assertEqual(result.strip(), "")

    def test_initial_tmpl(self):
        result = create_base()
        expected = """var wutu = angular.module("wutu", []);"""
        self.assertEqual(result.strip(), expected)