class HttpService(object):
	"""
	Generator for AngularJS $http
	"""
	def get(self, url, _id):
		return "$http.get({0} + \"/\" + {1} + \"/\");".format(url, " + \"/\" + ".join(_id))

	def post(self, url, _id, data="data"):
		return "$http.post({0} + \"/\" + {1} + \"/\", {2});".format(url, " + \"/\" + ".join(_id), data)

	def put(self, url, data="data"):
		return "$http.put({0}, {1});".format(url, data)

	def delete(self, url, _id):
		return "$http.delete({0} + \"/\" + {1} + \"/\");".format(url, " + \"/\" + ".join(_id))
