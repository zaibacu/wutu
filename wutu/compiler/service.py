def create_service_js(stream, module):
    """
    Creates AngularJS service from module
    :param stream:
    :param module:
    :return:
    """
    from wutu.util import get_implemented_methods
    from wutu.compiler.grammar import Provider, Function, Object, SimpleDeclare, String, Expression
    stream.write("wutu.factory('{0}Service', ['$http', ".format(module.__class__.__name__))
    http = Provider("$http")
    params = module.get_identifier()
    obj = Object()
    full_url = "base_url() + url + \"/\" + {0} + \"/\"".format(" + \"/\" + ".join(params))
    obj.add_member("get", Function(params=params, returns=http.get(full_url)))
    obj.add_member("put", Function(params=("data",), returns=http.put("base_url() + url", "data")))
    obj.add_member("post", Function(params=params + ("data",), returns=http.post(full_url, "data")))
    obj.add_member("delete", Function(params=params, returns=http.delete(full_url)))
    impl = Function([http.name],
                    body=[SimpleDeclare("url", String(module.__name__)), SimpleDeclare("service", obj, private=True)],
                    returns=Expression("service"))
    stream.write(impl.compile())
    stream.write("]);\n")
