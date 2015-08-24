from selenium import webdriver
from flask.ext.testing import LiveServerTestCase
import unittest
from multiprocessing import Process

from wutu import app
from test_util import *

class Functional(LiveServerTestCase):
    def create_app(self):
        return app.create(index="test.html",
                        locator=test_locator,
                        host="localhost",
                        port=5555,
                        debug=True,
                        use_reloader=False,
                        testing=True)


    def setUp(self):
        self.browser = webdriver.PhantomJS()

    def tearDown(self):
        self.browser.close()

    def test_module_get(self):
        self.browser.get(self.get_server_url())
        self.assertEqual(self.browser.title, "test")
