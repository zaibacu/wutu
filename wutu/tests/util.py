import os


class ApiMock(object):
	def add_resource(self, res, *args):
		pass

def test_locator(*dir):
	return os.path.join(os.path.dirname(os.path.realpath(__file__)), *dir)