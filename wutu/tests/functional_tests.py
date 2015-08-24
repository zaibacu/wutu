from selenium import webdriver
import unittest
from multiprocessing import Process
from urllib.request import urlopen

from wutu import app
from test_util import *

TEST_HOST = "localhost"
TEST_PORT = 5555
def get_server_url():
    return "http://{0}:{1}".format(TEST_HOST, TEST_PORT)

def start_server():
    testing_app = app.create(index="test.html", locator=test_locator)
    testing_app.run(host=TEST_HOST, port=TEST_PORT, debug=True, use_reloader=False)

class Functional(unittest.TestCase):
    def setUp(self):
        self.p = Process(target=start_server)
        self.p.start()
        self.browser = webdriver.PhantomJS()


    def tearDown(self):
        self.browser.close()
        self.p.terminate()

    def test_module_index(self):
        self.browser.get(get_server_url())
        self.assertEqual(self.browser.title, "test")
        print(self.browser.page_source)

    def test_module_controller(self):
        self.browser.get("{0}/test_module/controller.js".format(get_server_url()))
        self.assertTrue(len(self.browser.page_source) > 0)

    def test_module_service(self):
        self.browser.get("{0}/test_module/service.js".format(get_server_url()))
        self.assertTrue(len(self.browser.page_source) > 0)


