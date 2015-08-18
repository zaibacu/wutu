from wutu.module import Module


class TestModule(Module):
    def __init__(self):
        super(TestModule, self).__init__()

    def ping(self):
        return "pong"

    def get(self):
        return {"result": "Hello"}
