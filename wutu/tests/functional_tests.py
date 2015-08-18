from selenium import webdriver
import unittest
from multiprocessing import Process

from wutu import app

def start_server():
    app.main(host="localhost", port=5555, debug=True)


class Functional(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.close()

    def test_module_get(self):
        self.browser.get("http://localhost:5555/")

if __name__ == "__main__":
    p = Process(target=start_server)
    p.start()
    unittest.main(warnings=False)
