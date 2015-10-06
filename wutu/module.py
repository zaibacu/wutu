from flask_restful import Resource
from wutu.compiler.common import *
from wutu.compiler.service import *
from wutu.compiler.controller import *
from wutu.decorators import stub


class Module(Resource):
    """
    Base class for all modules
    """
    def __init__(self):
        super(Module, self).__init__()
        self.compile_service = True
        self.compile_module = True

    @stub
    def get(self):
        """
        Responds to GET request
        """

    @stub
    def post(self):
        """
        Responds to POST request
        """

    @stub
    def put(self):
        """
        Responds to PUT request
        """

    @stub
    def delete(self):
        """
        Responds to DELETE request
        """

    @staticmethod
    def mediatypes():
        """
        Mediatypes override
        :return:
        """
        return ["application/json", "text/javascript"]

    def create_service(self, stream):
        """
        Constructs AngularJS service
        :param stream:
        :return:
        """
        create_service_js(stream, self)

    def create_controller(self, stream):
        """
        Constructs AngularJS controller
        :param stream:
        :return:
        """
        create_controller_js(stream, self)

    def get_service(self):
        """
        Constructs AngularJS service without stream
        :return:
        """
        stream = create_stream()
        self.create_service(stream)
        return get_data(stream)

    def get_controller(self):
        """
        Returns AngularJS controller
        :return:
        """
        stream = create_stream()
        self.create_controller(stream)
        return get_data(stream)

    def get_name(self):
        """
        Returns module name
        :return:
        """
        return self.__name__

    def get_identifier(self):
        """
        Returns Ids for this module
        :return:
        """
        from wutu.util import get_identity
        return get_identity(self)

    def get_entity_name(self):
        """
        Returns entity name to be used in naming methods in Controller
        :return:
        """
        return self.__name__

    @staticmethod
    def get_request_data():
        """
        Returns request data
        :return:
        """
        from wutu.util import get_request_json
        return get_request_json()

