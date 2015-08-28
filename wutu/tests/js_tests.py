import unittest
from Naked.toolshed.shell import execute_js, execute, muterun
from multiprocessing import Process
from test_util import *
import time


def start_selenium():
	muterun("./node_modules/protractor/bin/webdriver-manager start")


class JsTests(unittest.TestCase):
	def setUp(self):
		execute("npm install")
		execute("./node_modules/protractor/bin/webdriver-manager update")
		prepare_db()
		self.p = Process(target=start_server)
		self.p.start()

	def tearDown(self):
		self.p.terminate()

	def test_run_unit_tests(self):
		result = execute("./node_modules/karma/bin/karma start")
		self.assertTrue(result)

	def test_run_e2e_tests(self):
		selenium = Process(target=start_selenium)
		selenium.start()
		time.sleep(5)
		result = execute("./node_modules/protractor/bin/protractor e2e.conf.js")
		self.assertTrue(result)
		selenium.terminate()
