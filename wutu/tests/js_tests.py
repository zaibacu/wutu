import unittest
from Naked.toolshed.shell import execute_js
from test_util import *
from wutu.util import load_module

class JsTests(unittest.TestCase):
    def setUp(self):
        mod = load_module("test_module", test_locator)
        with open("tmp/test_module_service.js", "w") as f:
            f.write(mod.get_service())

    def test_validate_syntax(self):
        self.assertTrue(execute_js("tmp/test_module_service.js"))
