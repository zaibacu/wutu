
def create_service_js(module):
    tmpl = """
        wutu.factory("{0}Service", ["$http", function($http){{
            var url = "/{2}";
            var service = {{
                get: function({1}){{
                    return $http.get(url + "/" {1});
                }},
                put: function({1}, data){{
                    return $http.put(url + "/" {1}, data);
                }},
                post: function({1}, data){{
                    return $http.post(url + "/" {1}, data);
                }},
                delete: function({1}){{
                    return $http.delete(url + "/" {1});
                }}
            }};
            return service;
        }}]);
    """.format(module.__class__.__name__, module.get_identifier(), module.__name__)

    return tmpl