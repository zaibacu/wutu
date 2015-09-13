from functools import wraps


def stub(fn):
	"""
	Used for unimplemeted parent class methods.
	Warns about it upon usage
	:param fn: method
	"""
	@wraps(fn)
	def wrapper(*args, **kwargs):
		raise NotImplemented("Method {0} is not implemented. Method desc: {1}".format(fn.__name__, fn.__doc__))
	return wrapper


def inject_module(module):
	"""
	Decorator which loads and passes module as a parameter
	:param module: module name
	:return: wrapped function
	"""
	from wutu.util import load_module
	mod = load_module(module)

	def injector(fn):
		@wraps(fn)
		def wrapper(*args, **kwargs):
			kwargs["module"] = mod
			fn(*args, **kwargs)
		return wrapper
	return injector


def create_module(api, name=None):
	"""
	A decorator which dynamically creates and binds new module
	:param api: flask_restful api endpoint
	:param name: optional name override for module. If not defined, automatically picked from function name
	:return:
	"""
	from wutu.util import get_logger, camel_case_name, class_factory, setup_endpoint
	from wutu.module import Module

	def injector(fn):
		log = get_logger("Decorators")
		nonlocal name
		if not name:
			name = fn.__name__
		ctr = class_factory(camel_case_name(name), Module, **fn())
		inst = ctr()
		setup_endpoint(api, inst, name)
		inst.create_service(api.jsstream)
		inst.create_controller(api.jsstream)
		log.info("Module '{0}' created".format(name))

	return injector

