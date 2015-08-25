import unittest
from Naked.toolshed.shell import execute_js, execute
from multiprocessing import Process
from test_util import *

class JsTests(unittest.TestCase):
    def setUp(self):
        execute("npm install")
        self.p = Process(target=start_server)
        self.p.start()

    def tearDown(self):
        self.p.terminate()

    def test_run_unit_tests(self):
        result = execute("./node_modules/karma/bin/karma start")
        self.assertTrue(result)
