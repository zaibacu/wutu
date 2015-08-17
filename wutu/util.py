import os


def get_modules():
	return os.listdir(current("modules"))

def current(dir):
	return os.path.join(os.getcwd(), dir)