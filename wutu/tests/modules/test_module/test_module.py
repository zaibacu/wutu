from wutu.module import Module


class TestModule(Module):
    def ping(self):
        return "pong"
