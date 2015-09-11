import os
import inspect
import tempfile
from flask import Response, request
from logbook import Logger
from contextlib import contextmanager
from wutu.module import Module
from functools import lru_cache
modules = []


def get_logger(name):
	"""
	Returns a logging provider
	:param name: name for logger
	:return: logger
	"""
	return Logger(name)

log = get_logger("util")


def location(directory):
	"""
	:param directory: Directory in usual unix convention
	:return: OS-specialized
	"""
	return os.path.join(*directory.split("/"))


def get_modules():
	"""
	Returns currently loaded modules
	:return:
	"""
	return modules


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
	:param: kwargs: optional params
	:return:
	"""
	def __init__(self, **options):
		for key, val in options.items():
			setattr(self, key, val)
		self.__name__ = endpoint_name(name)
		base.__init__(self)

	struct = {"__init__": __init__}
	struct.update(kwargs)
	ctr = type(name, (base,), struct)
	return ctr


def endpoint_name(name):
	"""
	Converts string from CameCase to under_score_case
	:param name: regular name
	:return:
	"""
	LState = class_factory("LState", object)
	UState = class_factory("UState", object)

	state = UState
	words = []
	cur = []
	for l in name:
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


def camel_case_name(name):
	"""
	Converts string to CamelCase
	:param name: input string
	:return: CamelCased string
	"""
	return "".join([words[0].upper() + words[1:] for words in name.split("_")])


def get_identity(inst):
	"""
	Returns required positional arguments for module
	:param inst: module instance
	:return:
	"""
	return list(filter(lambda x: x != "self", inspect.getargspec(inst.get).args))


def setup_endpoint(api, inst, name):
	"""
	Binds module to API
	:param api: Flask-Restful
	:param inst: module instance
	:param name: end-point name
	"""

	params = "/".join(["<{0}>".format(param) for param in get_identity(inst)])
	api.add_resource(inst, "/{0}".format(name), "/{0}/{1}/".format(name, params))
	global modules
	modules.append(inst)

	@api.app.route("/{0}/service.js".format(name), endpoint="{0}.service_endpoint".format(name))
	@lru_cache()
	def get_service_endpoint():
		"""
		Endpoint for AngularJS service (Generated)
		"""
		return Response(inst.get_service(), mimetype="text/javascript")

	@api.app.route("/{0}/controller.js".format(name), endpoint="{0}.controller_endpoint".format(name))
	@lru_cache()
	def get_controller_endpoint():
		"""
		Endpoint for AngularJS controller (User defined)
		"""
		return Response(inst.get_controller(), mimetype="text/javascript")


def load_module(module, api=None):
	"""
	Loads selected module
	:param module: module name
	:param api: parameter for automatic binding
	:return: module instance
	"""
	mod = __import__("{0}".format(module), globals(), locals(), fromlist=["*"])
	for _, m in inspect.getmembers(mod, inspect.ismodule):
		for _, cls in inspect.getmembers(m, inspect.isclass):
			if issubclass(cls, Module) and cls != Module:
				inst = cls()
				name = endpoint_name(cls.__name__)
				inst.__name__ = name
				if api:
					setup_endpoint(api, inst, name)
				return inst


def load_modules(locator=current):
	"""
	Returns list of modules in directory
	:param locator: function which tells where to look for modules
	:return: list of module names
	"""
	try:
		blacklist = ["__pycache__", "__init__.py", ".DS_Store"]
		modules = list(filter(lambda name: name not in blacklist, os.listdir(locator("modules"))))
		log.info("{0} modules loaded".format(len(modules)))
		return modules
	except FileNotFoundError:
		log.error("Failed to load modules from: '{0}'. Maybe incorrect directory?".format(locator("modules")))
		return []


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


def get_request_args():
	"""
	Returns arguments passed to request
	:return:
	"""
	return request.args


@contextmanager
def temp_file():
	"""
	Creates a temp file and deletes it afterwards
	:return:
	"""
	temp = tempfile.NamedTemporaryFile(delete=False)
	try:
		yield temp
	finally:
		temp.close()
		os.unlink(temp.name)


@contextmanager
def timer(title):
	"""
	Measures time elapsed in current block
	:param title: Name of block to be visible in output
	:return:
	"""
	from time import perf_counter as pc
	start = pc()
	try:
		yield
	finally:
		timediff = (pc() - start) * 1000
		log.debug("It took {0} ms to execute block '{1}'".format(timediff, title))

