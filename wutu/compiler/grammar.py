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


class Arg(object):
    def __init__(self, onstr: str, oncall: Callable):
        self.onstr = onstr
        self.oncall = oncall

    def compile(self):
        return self.onstr

    def __call__(self, *args, **kwargs):
        return self.oncall(*args, **kwargs)


class Provider(object):
    """
    A dynamic class which itself is not compilable, but its methods - are
    """
    def __init__(self, name):
        self.name = name
        self.assignments = []

    def __getattr__(self, item: str) -> Callable:
        if item in self.__dict__:
            return self[item]

        def caller(*args: List[str]) -> Compilable:
            content = "{0}.{1}({2})".format(self.name, item, ",".join(args))
            return Promise(content)

        return Arg(Expression("{0}.{1}".format(self.name, item)).compile(), caller)

    def __setattr__(self, key: str, value: str):
        special = {"name", "assignments"}
        if key in special:
            super().__setattr__(key, value)
        else:
            self.assignments.append(SimpleDeclare("{0}.{1}".format(self.name, key), value))

    def __setitem__(self, key: str, value: str):
        return self.__setattr__(key, value)

    def __getitem__(self, key: str):
        return self.__getattr__(key)


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
        return "{0} {1} = {2};".format("var" if self.private else "", self.name, self.value).strip()


class Object(Compilable):
    """
    Class builder
    """
    def __init__(self):
        self.members = []

    def compile(self):
        body = ",\n".join(["\"{0}\": {1}".format(key, val.compile()) for key, val in self.members])
        content = "{{\n {0} \n}}".format(body)

        return content

    def add_member(self, name: str, content: Compilable):
        self.members.append((name, content))


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
            return "\n\t".join([comp.compile() for comp in self.body])

        def create_return():
            if self.returns:
                return "\treturn {0};".format(self.returns.compile())
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


def unwraps(promise: Promise=None, parent: str=None) -> tuple:
    """
    A helper function which unwraps promise by executing and returning result inline.
    :param promise: promise function to unwrap
    :param parent: provide parent parameter name if desired to fill existing variable
    :returns: 'body', 'returns'. To be used as Function object parameter
    """
    body = []
    if parent:
        result_val = parent
    else:
        body.append(SimpleDeclare("result", "[]", private=True))
        result_val = "result"

    body.append(Expression("if({0} !== undefined){{".format(result_val)))
    body.append(Expression(promise.resolve(Function(["response"],
                                                    body=[
                                                        Expression("""
                                                        angular.forEach(response.data, function(val){{
                                                            {0}.push(val);
                                                            }})
                                                        """.format(result_val))]))))
    body.append(Expression("}} else {{ return {0}; }}".format(
        promise.resolve(Function(["response"],
                                 returns=Expression("response.data")))))
    )
    returns = Expression(result_val)
    return body, returns
