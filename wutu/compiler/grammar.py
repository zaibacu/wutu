import abc
from typing import Any


class Compileable(abc.ABC):
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


class Variable(Compileable):
    """
    A base for variables
    """
    def __init__(self, value: Any):
        self.value = value


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


class SimpleDeclare(Compileable):
    """
    Builder for variable declaration
    """
    def __init__(self, name: str, value: Compileable, private: bool=False):
        self.name = name
        self.value = value
        self.private = private

    def compile(self):
        return "{0} {1} = {2};".format("var" if self.private else "", self.name, self.value)
