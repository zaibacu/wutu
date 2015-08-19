from selenium import webdriver
import unittest
from multiprocessing import Process

from wutu import app
from test_util import *

def start_server():
    app.main(index="test.html", locator=test_locator, host="localhost", port=5555, debug=True, use_reloader=False)


class Functional(unittest.TestCase):
    def setUp(self):
        self.p = Process(target=start_server)
        self.p.start()
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.close()
        self.p.terminate()

    def test_module_get(self):
        self.browser.get("http://localhost:5555/")
        self.assertEqual(self.browser.title, "test")
