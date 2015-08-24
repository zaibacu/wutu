from flask_restful import Resource
from compiler import *
import os
import sys
import inspect

def module_locator(module, *dir):
    get_module_dir = lambda mod: \
                            os.path.dirname(
                                inspect.getmodule(mod.__class__).__file__
                            )
    return os.path.join(get_module_dir(module), *dir)

class Module(Resource):
    def __init__(self):
        super(Module, self).__init__()

    def mediatypes(self):
        return ["application/json", "text/javascript"]

    def create_service(self, stream):
        create_service_js(stream, self)

    def get_service(self):
        stream = create_stream()
        self.create_service(stream)
        return get_data(stream)

    def get_controller(self):
        return ""

    def get_identifier(self):
        return ["id"]

    def get_name(self):
        return self.__name__