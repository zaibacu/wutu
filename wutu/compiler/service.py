import inspect
from collections import namedtuple


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
		from wutu.compiler.common import function_block, indent_wrapper
		if not self._is_first():
			self.stream.write(",\n")
		else:
			self.first = False

		stream = indent_wrapper(self.stream)
		stream.write("{0}:".format(name))
		with function_block(stream, args) as block:
			fn(block)


def create_service_js(stream, module):
	"""
	Creates AngularJS service from module
	:param stream:
	:param module:
	:return:
	"""
	from wutu.compiler.http import HttpService
	from wutu.compiler.common import function_block, add_variable, service_block
	http = HttpService()
	struct = namedtuple("Mapping", ["args", "fn"])

	args = module.get_identifier()
	methods = dict(inspect.getmembers(module.__class__, predicate=inspect.isfunction))

	mapping = { "get": struct(args, lambda s: s.write("return " + http.get("base_url() + url", args))),
				"post": struct((args + ("data",)), lambda s: s.write("return " + http.post("base_url() + url", args, "data"))),
				"delete": struct(args, lambda s: s.write("return " + http.delete("base_url() + url", args))),
				"put": struct(("data",), lambda s: s.write("return " + http.put("base_url() + url", "data")))}

	filtered = {key: mapping[key] for key in (methods.keys() & mapping.keys()) if "Module.{0}".format(key) not in methods[key].__qualname__}
	stream.write("wutu.factory(\"{0}Service\", [\"$http\", ".format(module.__class__.__name__))
	with function_block(stream, ["$http"]) as block:
		add_variable(block, "url", module.__name__)
		with service_block(stream) as service:
			for key, val in filtered.items():
				service.add_method(key, val.args, val.fn)

	stream.write("]);\n")
