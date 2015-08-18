import os
import configparser
import importlib

def current(*dir):
	return os.path.join(os.getcwd(), *dir)

def load_module_config(module, locator=current):
	conf = configparser.ConfigParser()

	loadDir = locator("modules", module, "module.ini")
	conf.read(loadDir)
	return conf

def load_module(module, locator=current, api=None):
	conf = load_module_config(module, locator)
	name = conf.get("DEFAULT", "module_name")
	mod = importlib.import_module("modules.{0}.{1}".format(module, name))
	inst = getattr(mod, conf.get("DEFAULT", "class_name"))()
	if api:
		api.add_resource(inst, "/{0}/".format(name))
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
	return list(filter(lambda mod: is_module_enabled(mod, locator),  modules))