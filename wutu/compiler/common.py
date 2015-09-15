from io import StringIO
from contextlib import contextmanager
import numbers
from wutu.compiler.service import ServiceObj


def add_variable(stream, name, value, private=True):
	"""
	Adds JavaScript variable
	:param stream:
	:param name: variable name
	:param value: variable value
	:param private: should it be declared as private?
	:return:
	"""
	if private:
		stream.write("var ")

	def format_value(val):
		if isinstance(val, numbers.Number):
			return val
		elif isinstance(val, str):
			return "\"{0}\"".format(val)
		elif callable(val):
			return val()
		else:
			raise NotImplementedError("Not supported... Yet")

	stream.write("{0} = {1};\n".format(name, format_value(value)))


def create_base(stream):
	"""
	Base data to init AngularJS
	:param stream:
	:return:
	"""
	add_variable(stream, "base_url", lambda: "function(){ return \"/\"; }")
	add_variable(stream, "wutu", lambda: "angular.module(\"wutu\", [])")


def create_stream():
	"""
	Constructs stream
	:return:
	"""
	return StringIO()


def get_data(stream):
	"""
	Gets data from stream
	:param stream:
	:return:
	"""
	stream.seek(0)
	return stream.read()


def indent_wrapper(stream):
	"""
	Automatic indent handling
	:param stream:
	:return:
	"""
	class Wrapper(object):
		def write(self, msg):
			stream.write("\t" + msg)
	return Wrapper()


@contextmanager
def function_block(stream, params):
	"""
	Automatic function block handling
	:param stream:
	:param params:
	:return:
	"""
	stream.write("function({0}){{\n".format(", ".join(params)))
	try:
		yield indent_wrapper(stream)
	finally:
		stream.write("\n")
		stream.write("}")


@contextmanager
def service_block(stream):
	"""
	Init service wrapper
	:param stream:
	:return:
	"""
	service = ServiceObj(stream)
	service.write_header()
	try:
		yield service
	finally:
		service.write_footer()

