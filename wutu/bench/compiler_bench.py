from wutu.compiler.common import create_stream
from wutu.compiler.service import create_service_js
from wutu.compiler.controller import create_controller_js
from wutu.util import *


def handle_creation(module, stream):
    create_service_js(stream, module)
    create_controller_js(stream, module)


def main():
    mod = Module()
    mod.__name__ = "test_module"
    stream = create_stream()
    for i in range(0, 1000):
        handle_creation(mod, stream)

if __name__ == "__main__":
    import cProfile
    cProfile.run("main()")
