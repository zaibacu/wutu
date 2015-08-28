import os
from wutu import app
from wutu.util import *


class AppMock(object):
	@staticmethod
	def route(rule, endpoint, **options):
		def injector(fn):
			def wrapper(*args, **kwargs):
				return fn(*args, **kwargs)
			return wrapper
		return injector


class ApiMock(object):
	app = AppMock()

	def __init__(self):
		self.log = get_logger("api_mock")
		self.resources = {}

	def add_resource(self, res, *args):
		for endpoint in args:
			self.log.info("Registering {0} endpoint".format(endpoint))
			self.resources[endpoint] = res

	def call(self, endpoint, method, *args):
		def do_call(inst):
			return getattr(inst, method)(*args)

		return do_call(self.resources[endpoint])


def test_locator(*directory):
	return os.path.join(os.path.dirname(os.path.realpath(__file__)), *directory)


def remove_whitespace(_str):
	def ignore(x):
		chars = [' ', '\t', '\n']
		return x in chars
	return "".join(list(filter(lambda x: not ignore(x), _str)))


def normalize_slashes(_str):
	return _str.replace("\\", "/")


def compare(fn, str1, str2):
	return fn(remove_whitespace(str1), remove_whitespace(str2))


def compare_dir(fn, str1, str2):
	return fn(normalize_slashes(str1), normalize_slashes(str2))

TEST_HOST = "localhost"
TEST_PORT = 5555


def get_server_url():
	return "http://{0}:{1}".format(TEST_HOST, TEST_PORT)


def start_server():
	testing_app = app.create(index="test.html", locator=test_locator)
	testing_app.run(host=TEST_HOST, port=TEST_PORT, debug=True, use_reloader=False)
