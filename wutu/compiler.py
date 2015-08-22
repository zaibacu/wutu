from io import StringIO
from contextlib import contextmanager


def create_service_js(module):
    tmpl = """
        wutu.factory("{0}Service", ["$http", function($http){{
            var url = "/{2}";
            var service = {{
                get: function({1}){{
                    return $http.get(url + "/" + {1});
                }},
                put: function({1}, data){{
                    return $http.put(url + "/" + {1}, data);
                }},
                post: function({1}, data){{
                    return $http.post(url + "/" + {1}, data);
                }},
                delete: function({1}){{
                    return $http.delete(url + "/" + {1});
                }}
            }};
            return service;
        }}]);
    """.format(module.__class__.__name__, module.get_identifier(), module.__name__)

    return tmpl

def create_base():
    tmpl = """
            var wutu = angular.module("wutu", []);
        """
    return tmpl

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

