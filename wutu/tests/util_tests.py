import unittest
from wutu.test_util import *
from wutu.decorators import *
from wutu.compiler.common import get_data


class UtilTests(unittest.TestCase):
    def setUp(self):
        self.api = ApiMock()

    def test_endpoint_name(self):
        result = endpoint_name("TestModule")
        expected = "test_module"
        compare_dir(self.assertEqual, expected, result)

    def test_camel_case_name(self):
        result = camel_case_name("test_module")
        expected = "TestModule"
        self.assertEqual(expected, result)

    def test_module_creator(self):
        @create_module(self.api)
        def new_module():
            return {"get": lambda req: "Hello, world!"}

        self.assertEqual("Hello, world!", self.api.call("/new_module", "get"))

    def test_module_identity(self):
        @create_module(self.api)
        def new_module():
            return {"get": lambda self, _id: "Hello, world!"}

        module = self.api.resources["/new_module"]
        result = get_identity(module)
        expected = ("_id",)
        self.assertEqual(expected, result)

    def test_module_creation(self):
        create_module(self.api)(test_module)
        self.assertIn("/test_module", self.api.resources.keys())

    def test_location(self):
        result = location("test/something/something/something test.js")
        expected = os.path.join("test", "something", "something", "something test.js")
        self.assertEqual(expected, result)
