import sys
import jinja2
from flask import Flask, render_template, Response
from flask_restful import Api

from wutu.util import *
from wutu.compiler import create_base, create_stream, get_data


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='{<',
        variable_end_string='>}',
    ))


def create(index, locator):
    app = CustomFlask(__name__)
    api = Api(app)
    app.jinja_loader = jinja2.FileSystemLoader(locator())
    modules = [load_module(module, api=api) for module in get_modules()]

    @app.route("/")
    def index_page():
        return render_template(index, modules=modules)

    @app.route("/init.js")
    def init_page():
        stream = create_stream()
        create_base(stream)
        return Response(get_data(stream), mimetype="text/javascript")

    return app

if __name__ == "__main__":
    create(sys.argv).run(sys.argv)
