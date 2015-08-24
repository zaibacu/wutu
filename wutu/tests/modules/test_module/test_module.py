from wutu.module import Module, module_locator
from wutu.util import load_js


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
        return load_js("controller.js", module_locator)
