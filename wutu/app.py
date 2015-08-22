import sys
import jinja2
from flask import Flask, render_template
from flask_restful import Api

from wutu.util import *
from compiler import create_base, create_stream, get_data

app = Flask(__name__)
api = Api(app)

def main(index, locator, *args, **kwargs):
    app.jinja_loader = jinja2.FileSystemLoader(locator())
    modules = [ load_module(module, api=api) for module in get_modules() ]

    @app.route("/")
    def index_page():
        def init():
            stream = create_stream()
            create_base(stream)
            return get_data(stream)
        return render_template(index, modules=modules, init=init)

    app.run(*args, **kwargs)

if __name__ == "__main__":
    main(sys.argv)