from flask_restful import Resource
from compiler import *


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

    def create_controller(self):
        pass

    def get_identifier(self):
        return "id"

    def get_name(self):
        return self.__name__