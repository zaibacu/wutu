import app
from util import create_module
from test_util import *

import os
import sys
os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../")
sys.path.append("modules/")

def start_server():
	prepare_db()

	testing_app = app.create(index="test.html", locator=test_locator)

	@create_module(testing_app.api)
	def test_module_2():
		return {"get": lambda req: "Hello"}

	@create_module(testing_app.api)
	def test_module_3():
		return {"get": lambda req, id: "Hello again, {0}".format(id)}

	testing_app.run(host="localhost", port=5555, debug=True, use_reloader=False)

if __name__ == "__main__":
	start_server()
