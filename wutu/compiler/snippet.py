from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader("wutu", "snippets"))


def compile_snippet(tmpl, **kwargs):
    """
    Compiles selected snipped with jinja2
    :param tmpl: snippet name
    :param kwargs: arguments passed to context
    :return: generated HTML
    """
    def wrapper(val):
        if isinstance(val, str):
            return "\"{0}\"".format(val)
        else:
            return val

    kwargs.update({"wrap": wrapper})
    template = env.get_template(tmpl)
    return template.render(**kwargs)
