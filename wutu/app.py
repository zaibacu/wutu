import sys
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)


def main(*args):
    app.run(*args)

if __name__ == "__main__":
    main(sys.argv)