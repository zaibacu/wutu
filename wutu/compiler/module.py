def create_module_js(stream, mod):
    """
    Creates AngularJS module for our module
    :param stream: api stream - to put data
    :param mod: our module
    :return:
    """
    from wutu.compiler.snippet import compile_snippet
    from wutu.compiler.common import create_stream, get_data
    inner_stream = create_stream()
    inner_stream.write(str(compile_snippet("angular_module.html", name=mod.get_name(), declare="mod")))
    yield inner_stream
    yield stream.write(str(compile_snippet("require_wrapper.html", content=get_data(inner_stream))))

