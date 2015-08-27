from wutu import app
from test_util import *


def start_server():
    testing_app = app.create(index="test.html", locator=test_locator)
    testing_app.run(host="localhost", port=5555, debug=True, use_reloader=False)

if __name__ == "__main__":
    start_server()
