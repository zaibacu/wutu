from wutu.compiler import create_service_js, create_stream
from wutu.util import *


def handle_creation(module, stream):
	create_service_js(stream, module)


def main():
	mod = Module()
	mod.__name__ = "test_module"
	stream = create_stream()
	handle_creation(mod, stream)

if __name__ == "__main__":
	import cProfile
	cProfile.run("main()")
