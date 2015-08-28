import os
import inspect
from flask import Response
from logbook import Logger

from wutu.module import Module


def get_logger(name):
	"""
	Returns a logging provider
	:param name: name for logger
	:return: logger
	"""
	return Logger(name)

log = get_logger("util")


def current(*directory):
	"""
	Locator service
	:param directory: what to look for
	:return: formed directory
	"""
	return os.path.join(os.getcwd(), *directory)


def class_factory(name, base, **kwargs):
	"""
	Dynamic class generator
	:param name: class name
	:param base: parent class
	:return:
	"""
	def __init__(self, **kwargs):
		for key, val in kwargs.items():
			setattr(self, key, val)
		self.__name__ = endpoint_name(name)
		base.__init__(self)

	struct = {"__init__": __init__}
	struct.update(kwargs)
	ctr = type(name, (base,), struct)
	return ctr


def endpoint_name(str):
	"""
	Converts string from CameCase to under_score_case
	:param str:
	:return:
	"""
	LState = class_factory("LState", object)
	UState = class_factory("UState", object)

	state = UState
	words = []
	cur = []
	for l in str:
		if state == UState and l.isupper():
			cur.append(l.lower())
		elif state == UState and l.islower():
			state = LState
			cur.append(l)
		elif state == LState and l.isupper():
			words.append("".join(cur))
			cur = [l.lower()]
			state = UState
		else:
			cur.append(l)

	words.append("".join(cur))
	return "_".join(words)


def camel_case_name(str):
	"""
	Converts string to CamelCase
	:param str: input string
	:return: CamelCased string
	"""
	return "".join([words[0].upper() + words[1:] for words in str.split("_")])


def setup_endpoint(api, inst, name):
	"""
	Binds module to API
	:param api: Flask-Restful
	:param inst: module instance
	:param name: end-point name
	"""
	params = "/".join(["<{0}>".format(param) for param in inst.get_identifier()])
	api.add_resource(inst, "/{0}".format(name), "/{0}/{1}/".format(name, params))

	@api.app.route("/{0}/service.js".format(name), endpoint="{0}.service_endpoint".format(name))
	def get_service_endpoint():
		"""
		Endpoint for AngularJS service (Generated)
		"""
		return Response(inst.get_service(), mimetype="text/javascript")

	@api.app.route("/{0}/controller.js".format(name), endpoint="{0}.controller_endpoint".format(name))
	def get_controller_endpoint():
		"""
		Endpoint for AngularJS controller (User defined)
		"""
		return Response(inst.get_controller(), mimetype="text/javascript")


def create_module(api, name=None):
	"""
	A decorator which dynamically creates and binds new module
	:param api: flask_restful api endpoint
	:param name: optional name override for module. If not defined, automatically picked from function name
	:return:
	"""
	def injector(fn):
		nonlocal name
		if not name:
			name = fn.__name__
		ctr = class_factory(camel_case_name(name), Module, **fn())
		inst = ctr()
		setup_endpoint(api, inst, name)
		log.info("Module '{0}' created".format(name))

	return injector


def load_module(module, locator=current, api=None):
	"""
	Loads selected module
	:param module: module name
	:param locator: function which tells where to look for modules
	:param api: parameter for automatic binding
	:return: module instance
	"""
	mod = __import__("modules.{0}".format(module), globals(), locals(), fromlist=["*"])
	for _, m in inspect.getmembers(mod, inspect.ismodule):
		for _, cls in inspect.getmembers(m, inspect.isclass):
			if issubclass(cls, Module) and cls != Module:
				inst = cls()
				name = endpoint_name(cls.__name__)
				inst.__name__ = name
				if api:
					setup_endpoint(api, inst, name)
				return inst


def inject_module(module, locator=current):
	"""
	Decorator which loads and passes module as a parameter
	:param module: module name
	:param locator: function which tells where to look for modules
	:return: wrapped function
	"""
	mod = load_module(module, locator)

	def injector(fn):
		def wrapper(*args, **kwargs):
			kwargs["module"] = mod
			fn(*args, **kwargs)
		return wrapper
	return injector


def get_modules(locator=current):
	"""
	Returns list of modules in directory
	:param locator: function which tells where to look for modules
	:return: list of module names
	"""
	modules = os.listdir(locator("modules"))
	log.info("{0} modules loaded".format(len(modules)))
	return modules


def load_js(file, locator=current):
	"""
	Loads JavaScript into memory
	:param file: javascript file
	:param locator: function which tells where to look for it
	:return: javascript as a string
	"""
	with open(locator(file)) as f:
		raw = f.read()

	return raw
