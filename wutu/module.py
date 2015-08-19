from flask_restful import Resource


class Module(Resource):
    def __init__(self):
        super(Module, self).__init__()

    def mediatypes(self):
        return ["application/json"]

    def get_service(self):
        pass

    def get_controller(self):
        pass

    def get_identifier(self):
        return "id"