from selenium import webdriver
import unittest
from multiprocessing import Process

from wutu import app
from wutu.test_util import *

def start_server():
    app.main(index="test.html", locator=test_locator(), host="localhost", port=5555, debug=True)


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.close()

    def test_module_get(self):
        self.browser.get("http://localhost:5555/")
        self.assertEqual(self.browser.title, "test")

if __name__ == "__main__":
    p = Process(target=start_server)
    p.start()
    unittest.main(warnings=False)
