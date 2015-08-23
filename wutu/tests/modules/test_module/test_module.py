from wutu.module import Module
from wutu.util import load_js
from test_util import test_locator


class TestModule(Module):
    def __init__(self):
        super(TestModule, self).__init__()

    def ping(self):
        return "pong"

    def get(self, id):
        return {"result": id}

    def get_identifier(self):
        return ["id"]

    def get_controller(self):
        return load_js("test_module/controller.js", test_locator)
