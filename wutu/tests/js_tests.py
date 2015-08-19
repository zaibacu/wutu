import unittest
from Naked.toolshed.shell import execute_js
from test_util import *
from wutu.util import load_module

class JsTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module("test_module", test_locator)
