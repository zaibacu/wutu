from io import StringIO
from contextlib import contextmanager
import numbers


def add_variable(stream, name, value, private=True):
    """
    Adds JavaScript variable
    :param stream:
    :param name: variable name
    :param value: variable value
    :param private: should it be declared as private?
    :return:
    """
    if private:
        stream.write("var ")

    def format_value(val):
        if isinstance(val, numbers.Number):
            return val
        elif isinstance(val, str):
            return "\"{0}\"".format(val)
        elif callable(val):
            return val()
        else:
            raise NotImplementedError("Not supported... Yet")

    stream.write("{0} = {1};\n".format(name, format_value(value)))


def create_base(stream, ngmodules=None):
    """
    Base data to init AngularJS
    :param stream:
    :return:
    """
    add_variable(stream, "base_url", lambda: "function(){ return \"/\"; }")
    modules = ngmodules if ngmodules else []
    if len(modules) > 0:
        modules_str = "'{0}'".format("', '".join(modules))
    else:
        modules_str = ""
    add_variable(stream, "wutu", lambda: "angular.module(\"wutu\", [{0}])".format(modules_str))


def create_stream():
    """
    Constructs stream
    :return:
    """
    return StringIO()


def get_data(stream):
    """
    Gets data from stream
    :param stream:
    :return:
    """
    stream.seek(0)
    return stream.read()


def indent_wrapper(stream):
    """
    Automatic indent handling
    :param stream:
    :return:
    """
    class Wrapper(object):
        def write(self, msg):
            stream.write("\t" + msg)
    return Wrapper()


@contextmanager
def promise_resolve(stream):
    """
    AngularJS promise resolve
    :param stream:
    :return:
    """
    stream.write(".then(")
    with function_block(stream, ["result"]) as block:
        try:
            yield block
        finally:
            pass
    stream.write(");")


@contextmanager
def function_block(stream, params):
    """
    Automatic function block handling
    :param stream:
    :param params:
    :return:
    """
    stream.write("function({0}){{\n".format(", ".join(params)))
    try:
        yield indent_wrapper(stream)
    finally:
        stream.write("\n")
        stream.write("}")

