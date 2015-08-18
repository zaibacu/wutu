from selenium import webdriver
import unittest

from wutu import app

app.main(host="localhost", port=5555, debug=True)


"""browser = webdriver.Firefox()
browser.get("http://localhost:5555/test_module")

assert "test" in browser.title"""