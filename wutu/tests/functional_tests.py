from selenium import webdriver
import unittest
from multiprocessing import Process
from urllib.request import urlopen

from test_util import *


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

    def test_module_controller(self):
        self.browser.get("{0}/test_module/controller.js".format(get_server_url()))
        self.assertTrue(len(self.browser.page_source) > 0)

    def test_module_service(self):
        self.browser.get("{0}/test_module/service.js".format(get_server_url()))
        self.assertTrue(len(self.browser.page_source) > 0)
