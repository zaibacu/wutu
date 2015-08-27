import os
import configparser
import inspect
from flask import Response
from logbook import Logger

from wutu.module import Module


def get_logger(name):
	return Logger(name)

log = get_logger("util")


def current(*dir):
	return os.path.join(os.getcwd(), *dir)


def endpoint_name(str):
	class LState(object):
		pass
	class UState(object):
		pass

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


def setup_endpoint(api, inst, name):
	params = "/".join(["<{0}>".format(param) for param in inst.get_identifier()])
	api.add_resource(inst, "/{0}".format(name), "/{0}/{1}/".format(name, params))

	@api.app.route("/{0}/service.js".format(name))
	def get_service_endpoint():
		return Response(inst.get_service(), mimetype="text/javascript")

	@api.app.route("/{0}/controller.js".format(name))
	def get_controller_endpoint():
		return Response(inst.get_controller(), mimetype="text/javascript")


def load_module(module, locator=current, api=None):
	mod = __import__("modules.{0}".format(module), globals(), locals(), fromlist=["*"])
	for _, m in inspect.getmembers(mod, inspect.ismodule):
		for _, cls in inspect.getmembers(m, inspect.isclass):
			if issubclass(cls, Module) and cls != Module:
				inst = cls()
				name = endpoint_name(cls.__name__)
				if api:
					setup_endpoint(api, inst, name)
				return inst


def inject_module(module, locator=current):
	mod = load_module(module, locator)

	def injector(fn):
		def wrapper(*args, **kwargs):
			kwargs["module"] = mod
			fn(*args, **kwargs)
		return wrapper
	return injector


def is_module_enabled(module, locator=current):
	conf = load_module_config(module, locator)
	return conf.getboolean("DEFAULT", "enabled")


def get_modules(locator=current):
	modules = os.listdir(locator("modules"))
	log.info("{0} modules loaded".format(len(modules)))
	return modules


def load_js(file, locator=current):
	with open(locator(file), "r") as f:
		raw = f.read()

	return raw
