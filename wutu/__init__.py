__all__ = ["app", "version", "util", "module"]

from typing import Callable, List


class Wutu(object):
    """
    an external API for Wutu Framework
    """
    def __init__(self, index: str, ngmodules: List[str]=None, minify: bool=False) -> None:
        from wutu import app
        self.app = app.create(index=index, ngmodules=ngmodules, minify=minify)

    def create_module(self, fn: Callable):
        """
        Creates a Wutu module from your defined function.
        This function must include dict with following (each is optional) methods:
        'get', 'post', 'put', 'delete' each corresponds to HTTP methods.
        Special methods:
            - 'get_controller' - returns AngularJS JavaScript controller text (Can provide using Wutu.load_js method)
            - 'get_service' - returns AngularJS JavaScript service text (auto-generated by default)
        :param fn: Module function. Module name is automatically generated from function name
        :return:
        """
        from wutu.decorators import create_module
        return create_module(self.app.api)(fn)

    def run(self, *args, **kwargs) -> None:
        """
        Runs web app. Arguments are same as Flask, including:
            - host: on which address to bind (default: localhost)
            - port: on which port to bind (default: 5000)
            - debug: show debug info on errors (default: False)
        :param args:
        :param kwargs:
        :return:
        """
        self.app.run(*args, **kwargs)

    @staticmethod
    def load_js(name: str) -> str:
        """
        Loads and exposes JavaScript file
        :param name: name of the file
        :return: JavaScript object
        """
        from wutu.util import load_js
        return load_js(name)
