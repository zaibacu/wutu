def create_controller_js(stream, module):
    """
    Creates AngularJS controller from module
    :param stream:
    :param module:
    :return:
    """
    from wutu.util import get_implemented_methods
    from wutu.compiler.grammar import Provider, Function, SimpleDeclare
    stream.write("wutu.controller('{0}Controller', ".format(module.__class__.__name__))
    service = Provider("{0}Service".format(module.__class__.__name__))
    scope = Provider("$scope")
    methods = get_implemented_methods(module)
    entity_name = "{0}_list".format(module.get_entity_name())
    params = module.get_identifier()
    post_params = params + ("data",)
    put_params = ("data",)

    scope[entity_name] = service.list()
    scope.refresh = Function(None, body=[SimpleDeclare(scope[entity_name].compile(), service.list())])
    scope["get_{0}".format(module.get_entity_name())] = Function(params, returns=service.get(*params))
    scope["create_{0}".format(module.get_entity_name())] = Function(put_params, body=[service.put(*put_params), scope.refresh()])
    scope["update_{0}".format(module.get_entity_name())] = Function(post_params, body=[service.post(*post_params), scope.refresh()])
    scope["remove_{0}".format(module.get_entity_name())] = Function(params, body=[service.delete(*params), scope.refresh()])
    impl = Function([scope.name, service.name], body=scope.assignments)
    stream.write(impl.compile())
    stream.write(");")
