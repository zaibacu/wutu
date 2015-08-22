import os


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

def compare(fn, str1, str2):
	return fn(remove_whitespace(str1), remove_whitespace(str2))