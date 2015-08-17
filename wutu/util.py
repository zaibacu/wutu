import os
import configparser


def is_module_enabled(module):
	conf = configparser.ConfigParser()
	conf.read(current("modules", module, "module.ini"))
	return conf.getboolean("DEFAULT", "enabled")

def get_modules():
	modules = os.listdir(current("modules"))
	return list(filter(lambda mod: is_module_enabled(mod),  modules))

def current(*dir):
	return os.path.join(os.getcwd(), *dir)