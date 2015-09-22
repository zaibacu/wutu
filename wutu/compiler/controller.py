

def create_controller_js(stream, module):
    """
    Creates AngularJS controller from module
    :param stream:
    :param module:
    :return:
    """
    from wutu.compiler.common import function_block
    serviceref = "{0}Service".format(module.__class__.__name__)
    stream.write("wutu.controller('{0}Controller', ".format(module.__class__.__name__))
    with function_block(stream, [serviceref]) as block:
        pass
    stream.write(");")
