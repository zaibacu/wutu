import abc
from typing import Any, List, Callable


class Compilable(abc.ABC):
    """
    A base class for all compileables
    """
    @abc.abstractmethod
    def compile(self) -> str:
        """
        :return: Compiled string
        """

    def __repr__(self):
        return self.compile()

    def __eq__(self, other: str) -> bool:
        return self.compile() == other


class Variable(Compilable):
    """
    A base for variables
    """
    def __init__(self, value: Any):
        self.value = value

    def compile(self) -> str:
        return ""


class Provider(object):
    """
    A dynamic class which itself is not compilable, but its methods - are
    """
    def __init__(self, name):
        self.name = name

    def __getattr__(self, item: str) -> Callable:
        def caller(*args: List[str]) -> str:
            content = "{0}.{1}(\"{2}\")".format(self.name, item, ",".join(args))
            return Promise(content)

        return caller

    def __setattr__(self, key: str, value: str) -> str:
        return "{0}.{1} = {2};"


class Expression(Variable):
    """
    For cases when expression is needed as a variable
    """
    def compile(self) -> str:
        return "{0}".format(self.value)


class String(Variable):
    """
    A string variable representation
    """
    def compile(self) -> str:
        return "\"{0}\"".format(self.value)


class Number(Variable):
    """
    A number variable representation
    """
    def compile(self) -> str:
        return "{0}".format(self.value)


class SimpleDeclare(Compilable):
    """
    Builder for variable declaration
    """
    def __init__(self, name: str, value: Compilable, private: bool=False):
        self.name = name
        self.value = value
        self.private = private

    def compile(self):
        return "{0} {1} = {2};".format("var" if self.private else "", self.name, self.value)


class Function(Compilable):
    """
    Function builder
    """
    def __init__(self, params: List=None, body: List=None, returns: Compilable=None):
        self.params = params if params else []
        self.body = body if body else []
        self.returns = returns

    def compile(self):
        def create_params():
            return ",".join(self.params)

        def create_body():
            return "\n".join([comp.compile() for comp in self.body])

        def create_return():
            if self.returns:
                return "return {0};".format(self.returns.compile())
            else:
                return ""

        return "function({0}){{\n {1} \n{2}\n}}".format(create_params(), create_body(), create_return())


class Promise(Compilable):
    def __init__(self, content):
        self.content = content

    def compile(self) -> str:
        return self.content

    def resolve(self, body: Function) -> str:
        return "{0}.then({1});".format(self.compile(), body.compile())
