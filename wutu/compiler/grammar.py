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