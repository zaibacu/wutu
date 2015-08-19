
def create_service_js(module):
    tmpl = """
        wutu.factory("{0}Service", function($http){{
        }});
    """.format(module.__class__.__name__)

    return tmpl