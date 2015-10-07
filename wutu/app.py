import sys
import jinja2
from flask import Flask, render_template
from flask_restful import Api
from functools import lru_cache

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


def create(index="index.html", ngmodules=None, minify=True, locator=current):
    """
    Creates wutu app
    :param index: html file for index page
    :param minify: Do we want to minify generated JavaScripts (should be False for debug purposes)
    :param locator: function which tells where to find templates
    :return:
    """
    app = CustomFlask(__name__)
    api = Api(app)
    app.jinja_loader = jinja2.FileSystemLoader(locator())
    api.jsstream = create_stream()
    create_base(api.jsstream, ngmodules)

    @app.route("/")
    def index_page():
        """
        Endpoint for base page
        :return:
        """
        try:
            return render_template(index)
        except IOError:
            return "Failed to render template {0}, error: Not found".format(index)

    @lru_cache()
    @app.route("/wutu.js")
    def wutu_js():
        if minify:
            from jsmin import jsmin
            jsdata = jsmin(get_data(api.jsstream))
        else:
            from jsbeautifier import beautify
            jsdata = beautify(get_data(api.jsstream))
        return Response(jsdata, mimetype="text/javascript")

    app.api = api
    return app
