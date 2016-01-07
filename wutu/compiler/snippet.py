from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader("wutu", "snippets"))


class Compiled(object):
    """
    A wrapper for compiled snippet code,
    to avoid be handled as a string
    """
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


def compile_snippet(tmpl, **kwargs):
    """
    Compiles selected snipped with jinja2
    :param tmpl: snippet name
    :param kwargs: arguments passed to context
    :return: generated HTML
    """
    def wrapper(val):
        import numbers
        if isinstance(val, numbers.Number):
            return val
        elif isinstance(val, str):
            return "\"{0}\"".format(val)
        elif callable(val):
            return val()
        else:
            raise NotImplementedError("Not supported... Yet")

    kwargs.update({"wrap": wrapper})
    template = env.get_template(tmpl)
    return Compiled(template.render(**kwargs))
