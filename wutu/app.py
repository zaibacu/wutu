import sys
import jinja2
from flask import Flask, render_template
from flask_restful import Api

from wutu.util import *

app = Flask(__name__)
api = Api(app)

def main(index, locator, *args, **kwargs):
    app.jinja_loader = jinja2.FileSystemLoader(locator())
    modules = [ load_module(module, api=api) for module in get_modules() ]
    @app.route("/")
    def index_page():
        return render_template(index, modules=modules)

    app.run(*args, **kwargs)

if __name__ == "__main__":
    main(sys.argv)