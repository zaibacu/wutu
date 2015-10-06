def create_controller_js(stream, module):
    """
    Creates AngularJS controller from module
    :param stream:
    :param module:
    :return:
    """
    from wutu.util import get_implemented_methods
    from wutu.compiler.grammar import Provider, Function
    stream.write("wutu.controller('{0}Controller', ".format(module.__class__.__name__))
    service = Provider("{0}Service".format(module.__class__.__name__))
    scope = Provider("$scope")
    methods = get_implemented_methods(module)
    params = module.get_identifier()
    scope["get_{0}".format(module.get_entity_name())] = Function(params, returns=service.get(*params))
    scope["create_{0}".format(module.get_entity_name())] = Function(params, returns=service.put(*params))
    scope["update_{0}".format(module.get_entity_name())] = Function(params, returns=service.post(*params))
    scope["remove_{0}".format(module.get_entity_name())] = Function(params, returns=service.get(*params))
    impl = Function([scope.name, service.name], body=scope.assignments)
    stream.write(impl.compile())
    stream.write(");")
