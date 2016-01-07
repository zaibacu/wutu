from io import StringIO
from contextlib import contextmanager
from .snippet import compile_snippet


def add_variable(stream, name, value, private=True):
    """
    Adds JavaScript variable
    :param stream:
    :param name: variable name
    :param value: variable value
    :param private: should it be declared as private?
    :return:
    """
    stream.write(str(compile_snippet("variable.html", local=private, name=name, value=value)))


def create_base(stream, ngmodules=None):
    """
    Base data to init AngularJS
    :param stream:
    :return:
    """
    add_variable(stream, "base_url", lambda: "function(){ return \"/\"; }")
    modules = ngmodules if ngmodules else []
    stream.write(str(compile_snippet("angular_module.html", name="wutu", dep=modules)))
    stream.write(str(compile_snippet("unwrap_directive.html")))


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


