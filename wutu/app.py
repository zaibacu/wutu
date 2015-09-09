import sys
import jinja2
from flask import Flask, render_template
from flask_restful import Api

from wutu.util import *
from wutu.compiler.common import create_base, create_stream, get_data


class CustomFlask(Flask):
	"""
	Enchanted Flask module
	"""
	jinja_options = Flask.jinja_options.copy()
	jinja_options.update(dict(
		variable_start_string='{<',
		variable_end_string='>}',
	))


def create(index="index.html", locator=current):
	"""
	Creates wutu app
	:param index: html file for index page
	:param locator: function which tells where to find templates
	:return:
	"""
	app = CustomFlask(__name__)
	api = Api(app)
	app.jinja_loader = jinja2.FileSystemLoader(locator())
	[load_module(module, api=api) for module in load_modules(locator)]

	@app.route("/")
	def index_page():
		"""
		Endpoint for base page
		:return:
		"""
		try:
			return render_template(index, modules=get_modules())
		except IOError:
			return "Failed to render template {0}, error: Not found".format(index)

	@app.route("/init.js")
	def init_page():
		"""
		Endpoint for JavaScript init
		:return:
		"""
		stream = create_stream()
		create_base(stream)
		return Response(get_data(stream), mimetype="text/javascript")

	app.api = api
	return app

if __name__ == "__main__":
	create(sys.argv).run(sys.argv)
