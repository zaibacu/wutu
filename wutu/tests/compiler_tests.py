import unittest
from wutu.test_util import *
from wutu.compiler.common import *
from wutu.compiler.controller import *
from wutu.compiler.snippet import *
from wutu.util import *


class CompilerTests(unittest.TestCase):

    def test_service(self):
        mod = Module()
        mod.__name__ = "test_module"
        stream = StringIO()
        create_base(stream)
        mod.create_service(stream)
        result = get_data(stream)
        expected = """
        """

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
        from wutu.compiler.grammar import Provider, String
        http = Provider("$http")
        result = http.get(String("http://google.com").compile())
        expected = "$http.get(\"http://google.com\")"
        self.assertEqual(expected, result)
        http.url = "my_url_generator()"
        self.assertEqual(["$http.url = my_url_generator();"], http.assignments)

    def test_promise(self):
        from wutu.compiler.grammar import Provider, Function, SimpleDeclare, String, Expression
        http = Provider("$http")
        result = http.get(String("http://google.com").compile()).resolve(Function(["result"],
                                                                body=[SimpleDeclare("$scope.test", Expression("result.data"))]))
        expected = """
        $http.get("http://google.com").then(function(result){
            $scope.test = result.data;
        });
        """
        compare(self.assertEqual, expected, result)

    def test_object(self):
        from wutu.compiler.grammar import Object, String
        obj = Object()
        obj.add_member("something", String("test"))
        result = obj.compile()
        expected = "{ \"something\": \"test\" }"
        compare(self.assertEqual, expected, result)

    def test_unwrap(self):
        from wutu.compiler.grammar import Function, Promise, Provider, String, unwraps
        http = Provider("$http")
        promise = http.get(String("http://google.com").compile())
        result = Function([], *unwraps(promise)).compile()
        expected = """
        function(){
            var result = [];
            if(result != undefined){
                $http.get("http://google.com").then(function(response){
                    angular.forEach(response.data,
                            function(val){
                                result.push(val);
                            })
                });
            }
            else {
                return $http.get("http://google.com").then(function(response){
                    return response.data;
                });
            }
            return result;
        }
        """

        compare(self.assertEqual, expected, result)


class SnippetsTests(unittest.TestCase):
    def test_local_variable(self):
        expected = "var foo = \"bar\";"
        result = compile_snippet("variable.html", local=True, name="foo", value="bar")
        self.assertEqual(expected, str(result))

    def test_local_variable_without_assign(self):
        expected = "var test;"
        result = compile_snippet("variable.html", local=True, name="test")
        self.assertEqual(expected, str(result))

    def test_fn_as_variable(self):
        expected = "helloMsg = alert(\"Hello, world!\");"
        fn_snippet = compile_snippet("function_call.html", name="alert", params=["\"Hello, world!\""])
        result = compile_snippet("variable.html", name="helloMsg", value=fn_snippet)
        self.assertEqual(expected, str(result))

    def test_fn_block(self):
        expected = """
        function hello(name){
            hello_str = "Hello, ";
            return hello_str + " " + name;
        }
        """
        fn_block = compile_snippet("block.html",
                                   statements=[compile_snippet("variable.html", name="hello_str", value="Hello, ")],
                                   returns="hello_str + \" \" + name"
                                   )

        result = compile_snippet("function_define.html",
                                 name="hello",
                                 params=["name"],
                                 content=fn_block)

        compare(self.assertEqual, expected, str(result))
