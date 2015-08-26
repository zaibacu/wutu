import os
from wutu import app

class ApiMock(object):
	def add_resource(self, res, *args):
		pass

def test_locator(*dir):
	return os.path.join(os.path.dirname(os.path.realpath(__file__)), *dir)

def remove_whitespace(str):
	def ignore(x):
		chars = [' ', '\t', '\n']
		return x in chars
	return "".join(list(filter(lambda x: not ignore(x), str)))

def normalize_slashes(str):
	return str.replace("\\", "/")

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