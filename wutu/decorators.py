def stub(fn):
	"""
	Used for unimplemeted parent class methods.
	Warns about it upon usage
	:param fn: method
	"""
	def wrapper(*args, **kwargs):
		raise NotImplemented("Method {0} is not implemented. Method desc: {1}".format(fn.__name__, fn.__doc__))
	return wrapper

