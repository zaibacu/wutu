from flask_restful import Resource
from wutu.compiler.common import *
from wutu.decorators import stub
import os, inspect


def module_locator(module, *directory):
	"""
	Custom locator for modules
	:param module: module itself
	:param directory: search directory
	:return:
	"""
	get_module_dir = lambda mod: os.path.dirname(inspect.getmodule(mod.__class__).__file__)
	return os.path.join(get_module_dir(module), *directory)


class Module(Resource):
	"""
	Base class for all modules
	"""
	def __init__(self):
		super(Module, self).__init__()

	@stub
	def get(self):
		"""
		Responds to GET request
		"""

	@stub
	def post(self):
		"""
		Responds to POST request
		"""

	@stub
	def put(self):
		"""
		Responds to PUT request
		"""

	@stub
	def delete(self):
		"""
		Responds to DELETE request
		"""

	@staticmethod
	def mediatypes():
		"""
		Mediatypes override
		:return:
		"""
		return ["application/json", "text/javascript"]

	def create_service(self, stream):
		"""
		Constructs AngularJS service
		:param stream:
		:return:
		"""
		create_service_js(stream, self)

	def get_service(self):
		"""
		Constructs AngularJS service without stream
		:return:
		"""
		stream = create_stream()
		self.create_service(stream)
		return get_data(stream)

	def get_controller(self):
		"""
		Returns AngularJS controller
		:return:
		"""
		return ""

	def get_name(self):
		"""
		Returns module name
		:return:
		"""
		return self.__name__

	def get_identifier(self):
		"""
		Returns Ids for this module
		:return:
		"""
		from wutu.util import get_identity
		return get_identity(self)
