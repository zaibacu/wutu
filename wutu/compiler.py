from io import StringIO
from contextlib import contextmanager
import numbers

def add_variable(stream, name, value, private = True):
    if private:
        stream.write("var ")
    def format_value(value):
        if isinstance(value, numbers.Number):
            return value
        elif isinstance(value, str):
            return "\"{0}\"".format(value)
        elif callable(value):
            return value()
        else:
            raise NotImplementedError("Not supported... Yet")

    stream.write("{0} = {1};".format(name, format_value(value)))

def create_service_js(stream, module):
    stream.write("wutu.factory(\"{0}Service\", [\"$http\", ".format(module.__class__.__name__))
    with function_block(stream, ["$http"]) as block:
        block.write("var url =  \"{0}\";".format(module.__name__))
        with service_block(stream) as service:
            id = module.get_identifier()
            params = lambda x: ", ".join(x)
            service.add_method("get", id, lambda s:
                                                    s.write("return $http.get(base_url() + url + \"/\" + {0} + \"/\");".format(params(id))))
            service.add_method("put", ["data"], lambda s:
                                                            s.write("return $http.put(base_url() + url, data);"))
            service.add_method("post", id + ["data"], lambda s:
                                                            s.write("return $http.post(base_url() + url + \"/\" + {0} + \"/\", data);".format(params(id))))
            service.add_method("delete", id, lambda s:
                                                            s.write("return $http.delete(base_url() + url + \"/\" + {0} + \"/\");".format(params(id))))
    stream.write("])")

def create_base(stream):
    add_variable(stream, "base_url", lambda: "function(){ return \"/\"; };")
    add_variable(stream, "wutu", lambda: "angular.module(\"wutu\", [])")

def create_stream():
    return StringIO()

def get_data(stream):
    stream.seek(0)
    return stream.read()

@contextmanager
def function_block(stream, params):
    stream.write("function({0}){{\n".format(", ".join(params)))
    try:
        yield stream
    finally:
        stream.write("\n}")

class ServiceObj(object):
    def __init__(self, stream):
        self.stream = stream
        self.first = True

    def is_first(self):
        return self.first

    def write_header(self):
        self.stream.write("var service = {\n")

    def write_footer(self):
        self.stream.write("\n}\n return service;")

    def add_method(self, name, args, fn):
        if not self.is_first():
            self.stream.write(",\n")
        else:
            self.first = False

        self.stream.write("{0}:".format(name))
        with function_block(self.stream, args) as block:
            fn(self.stream)

@contextmanager
def service_block(stream):
    service = ServiceObj(stream)
    service.write_header()
    try:
        yield service
    finally:
        service.write_footer()

