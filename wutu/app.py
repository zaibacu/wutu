import sys
from flask import Flask
from flask_restful import Api

from wutu.util import *

app = Flask(__name__)
api = Api(app)


def main(*args, **kwargs):
    [ load_module(module, api=api) for module in get_modules() ]
    app.run(*args, **kwargs)

if __name__ == "__main__":
    main(sys.argv)