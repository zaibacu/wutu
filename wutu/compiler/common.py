from io import StringIO
from contextlib import contextmanager
import numbers
from wutu.compiler.http import HttpService


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


def create_service_js(stream, module):
	"""
	Creates AngularJS service from module
	:param stream:
	:param module:
	:return:
	"""
	stream.write("wutu.factory(\"{0}Service\", [\"$http\", ".format(module.__class__.__name__))
	with function_block(stream, ["$http"]) as block:
		add_variable(block, "url", module.__name__)
		with service_block(stream) as service:
			_id = module.get_identifier()
			http = HttpService()
			service.add_method("get", _id, lambda s:
				s.write("return " + http.get("base_url() + url", _id)))
			service.add_method("put", ["data"], lambda s:
				s.write("return " + http.put("base_url() + url", "data")))
			service.add_method("post", _id + ["data"], lambda s:
				s.write("return " + http.post("base_url() + url", _id, "data")))
			service.add_method("delete", _id, lambda s:
				s.write("return " + http.delete("base_url() + url", _id)))
	stream.write("]);\n")


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


class ServiceObj(object):
	"""
	AngularJS Service wrapper
	"""
	def __init__(self, stream):
		self.stream = stream
		self.first = True

	def _is_first(self):
		"""
		Is this method first
		"""
		return self.first

	def write_header(self):
		"""
		Write service header
		"""
		self.stream.write("var service = {\n")

	def write_footer(self):
		"""
		Write service footer
		"""
		self.stream.write("\n")
		self.stream.write("}")
		self.stream.write("\n")
		self.stream.write("return service;")

	def add_method(self, name, args, fn):
		"""
		Add method to service
		"""
		if not self._is_first():
			self.stream.write(",\n")
		else:
			self.first = False

		stream = indent_wrapper(self.stream)
		stream.write("{0}:".format(name))
		with function_block(stream, args) as block:
			fn(block)


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

