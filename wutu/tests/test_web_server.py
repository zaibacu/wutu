from wutu import Wutu
from wutu.test_util import prepare_db, test_module


def start_server():
	prepare_db()

	app = Wutu(index="test.html")

	@app.create_module
	def test_module_2():
		return {"get": lambda self: "Hello"}

	@app.create_module
	def test_module_3():
		return {"get": lambda self, id: "Hello again, {0}".format(id)}

	app.create_module(test_module)

	app.run(host="localhost", port=5555, debug=True, use_reloader=False)

if __name__ == "__main__":
	start_server()
