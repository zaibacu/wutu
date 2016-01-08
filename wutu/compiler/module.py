def create_module_js(stream, mod):
    """
    Creates AngularJS module for our module
    :param stream: api stream - to put data
    :param mod: our module
    :return:
    """
    from wutu.compiler.snippet import compile_snippet
    module = compile_snippet("angular_module.html", name=mod.get_name())
    stream.write(str(compile_snippet("require_wrapper.html", content=module)))
