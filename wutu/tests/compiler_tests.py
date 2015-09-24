import unittest
from wutu.test_util import *
from wutu.compiler.common import *
from wutu.compiler.http import HttpService
from wutu.compiler.controller import *
from wutu.util import *


class CompilerTests(unittest.TestCase):
    def test_initial_tmpl(self):
        stream = create_stream()
        create_base(stream)
        result = get_data(stream)
        expected = """
                var base_url = function(){ return "/"; };
                var wutu = angular.module("wutu", []);
            """
        compare(self.assertEqual, expected.strip(), result.strip())

    def test_function_block(self):
        stream = create_stream()
        with function_block(stream, ["test1", "test2"]) as block:
            block.write("console.log('Hello world!');")

        result = get_data(stream)
        expected = """
            function(test1, test2){
                console.log('Hello world!');
            }
        """
        compare(self.assertEqual, expected.strip(), result.strip())

    def test_service_block(self):
        stream = create_stream()
        with service_block(stream) as service:
            service.add_method("test_fn", ["test1", "test2"], lambda s: s.write("return true;"))
            service.add_method("test_fn2", ["test3"], lambda s: s.write("return false;"))

        result = get_data(stream)
        expected = """
            var service = {
             test_fn: function(test1, test2){
                return true;
             },
             test_fn2: function(test3){
                return false;
             }
            }
            return service;
        """
        compare(self.assertEqual, expected.strip(), result.strip())

    def test_string_argument(self):
        stream = create_stream()
        add_variable(stream, "test", "hello")
        result = get_data(stream).strip()
        excepted = "var test = \"hello\";"
        self.assertEqual(excepted, result)

    def test_int_argument(self):
        stream = create_stream()
        add_variable(stream, "test", 123)
        result = get_data(stream).strip()
        excepted = "var test = 123;"
        self.assertEqual(excepted, result)

    def test_module(self):
        mod = Module()
        mod.__name__ = "test_module"
        stream = StringIO()
        create_base(stream)
        mod.create_service(stream)
        self.assertTrue(validate_js(get_data(stream)))

    def test_forming_get(self):
        mod = Module()
        mod.__name__ = "test_module"
        mod.get = lambda self, _id: None
        http = HttpService()
        expected = """$http.get(base_url() + url + "/" + _id + "/");"""
        result = http.get("base_url() + url", mod.get_identifier())
        self.assertEqual(expected, result)

    def test_forming_post(self):
        mod = Module()
        mod.__name__ = "test_module"
        mod.get = lambda self, _id: None
        http = HttpService()
        expected = """$http.post(base_url() + url + "/" + _id + "/", data);"""
        result = http.post("base_url() + url", mod.get_identifier())
        self.assertEqual(expected, result)

    def test_forming_put(self):
        mod = Module()
        mod.__name__ = "test_module"
        mod.get = lambda self, _id: None
        http = HttpService()
        expected = """$http.put(base_url() + url, data);"""
        result = http.put("base_url() + url")
        self.assertEqual(expected, result)

    def test_forming_delete(self):
        mod = Module()
        mod.__name__ = "test_module"
        mod.get = lambda self, _id: None
        http = HttpService()
        expected = """$http.delete(base_url() + url + "/" + _id + "/");"""
        result = http.delete("base_url() + url", mod.get_identifier())
        self.assertEqual(expected, result)

    def test_forming_get_w_two_args(self):
        mod = Module()
        mod.__name__ = "test_module"
        mod.get = lambda self, _id, _id2: None
        http = HttpService()
        expected = """$http.get(base_url() + url + "/" + _id + "/" + _id2 + "/");"""
        result = http.get("base_url() + url", mod.get_identifier())
        self.assertEqual(expected, result)

    def test_forming_get_w_three_args(self):
        mod = Module()
        mod.__name__ = "test_module"
        mod.get = lambda self, _id, _id2, _id3: None
        http = HttpService()
        expected = """$http.get(base_url() + url + "/" + _id + "/" + _id2 + "/" + _id3 + "/");"""
        result = http.get("base_url() + url", mod.get_identifier())
        self.assertEqual(expected, result)


class GrammarTests(unittest.TestCase):
    def test_string(self):
        from wutu.compiler.grammar import String
        str = String("test")
        self.assertEqual("\"test\"", str.compile())

    def test_number(self):
        from wutu.compiler.grammar import Number
        num = Number(42)
        self.assertEqual("42", num.compile())

    def test_simple_declaration(self):
        from wutu.compiler.grammar import String, SimpleDeclare, Expression
        self.assertEqual("var foo = \"bar\";", SimpleDeclare("foo", String("bar"), True).compile())

    def test_function(self):
        from wutu.compiler.grammar import Function, String, SimpleDeclare, Expression
        fun = Function(["name"], [SimpleDeclare("hello_str", String("Hello, "))], Expression("hello_str + \" \" + name"))
        expected = """
        function(name){
            hello_str = "Hello, ";
            return hello_str + " " + name;
        }
        """
        compare(self.assertEqual, expected, fun.compile())

    def test_provider(self):
        from wutu.compiler.grammar import Provider
        http = Provider("$http")
        result = http.get("http://google.com")
        expected = "$http.get(\"http://google.com\")"
        self.assertEqual(expected, result)
        http.url = "my_url_generator()"
        self.assertEqual(["$http.url = my_url_generator();"], http.assignments)

    def test_promise(self):
        from wutu.compiler.grammar import Provider, Function, SimpleDeclare
        http = Provider("$http")
        result = http.get("http://google.com").resolve(Function(["result"],
                                                                body=[SimpleDeclare("$scope.test", "result.data")]))
        expected = """
        $http.get("http://google.com").then(function(result){
            $scope.test = result.data;
        });
        """
        compare(self.assertEqual, expected, result)
