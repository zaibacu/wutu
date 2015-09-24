from Naked.toolshed.shell import execute
import sqlite3
import json
from wutu.util import *
from wutu.compiler.common import create_stream
from wutu import Wutu
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "tests"))


class AppMock(object):
    @staticmethod
    def route(rule, endpoint, **options):
        def injector(fn):
            def wrapper(*args, **kwargs):
                return fn(*args, **kwargs)
            return wrapper
        return injector


class ApiMock(object):
    app = AppMock()

    def __init__(self):
        self.log = get_logger("api_mock")
        self.resources = {}
        self.jsstream = create_stream()

    def add_resource(self, res, *args):
        for endpoint in args:
            self.log.info("Registering {0} endpoint".format(endpoint))
            self.resources[endpoint] = res

    def call(self, endpoint, method, *args):
        def do_call(inst):
            return getattr(inst, method)(*args)

        return do_call(self.resources[endpoint])


def prepare_db():
    execute("rm testing.db")
    execute("touch testing.db") # Creates database for testing
    conn = sqlite3.connect("testing.db")
    query = """
        CREATE TABLE notes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        );
    """
    conn.cursor().execute(query)
    conn.commit()
    conn.close()


def test_locator(*directory):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "tests", *directory)


def remove_whitespace(_str):
    def ignore(x):
        chars = [' ', '\t', '\n']
        return x in chars
    return "".join(list(filter(lambda x: not ignore(x), _str)))


def normalize_slashes(_str):
    return _str.replace("\\", "/")


def compare(fn, str1, str2):
    return fn(remove_whitespace(str1), remove_whitespace(str2))


def compare_dir(fn, str1, str2):
    return fn(normalize_slashes(str1), normalize_slashes(str2))

TEST_HOST = "localhost"
TEST_PORT = 5555


def get_server_url():
    return "http://{0}:{1}".format(TEST_HOST, TEST_PORT)


def test_module():
    def get_connection():
        conn = sqlite3.connect("testing.db")
        return conn

    def get(self, _id):
        cursor = get_connection().cursor()
        if _id == "*":  # Wild Card
            return [{"id": row[0], "text": row[1]} for row in cursor.execute("SELECT id, text FROM notes")]
        else:
            return [{"id": row[0], "text": row[1]} for row in cursor.execute(
                "SELECT id, text FROM notes WHERE id = ?", int(_id))]

    def post(self, _id):
        data = json.loads(request.data.decode("utf-8"))
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE notes SET text=? WHERE id =", (data["text"], _id))
        conn.commit()
        return {"success": True}

    def put(self):
        data = json.loads(request.data.decode("utf-8"))
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes(text) VALUES(?)", (data["text"],))
        conn.commit()
        return {"id": cursor.lastrowid}

    def delete(self, _id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (_id,))
        conn.commit()
        return {"success": True}

    def create_controller(self, stream):
        stream.write("""
        wutu.controller("TestModuleController", function($scope, TestModuleService){
            $scope.data = {};
            TestModuleService.get("*").then(function(response){
                $scope.data = response.data;
            });

            $scope.add_note = function(text){
                TestModuleService.put({"text": text}).then(function(response){
                    $scope.data.push({"id": response.data.id, "text": text})
                });
            }

            $scope.delete_note = function(id){
                TestModuleService.delete(id).then(function(response){
                    $scope.data = $scope.data.filter(function(obj){
                        if(obj.id != id)
                            return true;
                    });
                });
            }
        });
        """)

    return {
        "get": get,
        "put": put,
        "post": post,
        "delete": delete,
        "create_controller": create_controller
    }


def start_server():
    """
    Starts a test server
    :return:
    """
    app = Wutu(index="test.html", minify=False)
    app.create_module(test_module)
    app.run(host=TEST_HOST, port=TEST_PORT, debug=True, use_reloader=False)


def validate_js(content):
    if not os.path.isfile(location("node_modules/jslint/bin/jslint.js")):
        raise RuntimeError("You're either missing nodejs package 'jslint', or 'npm' environment. ")
    with temp_file() as f:
        f.write(content.encode("UTF-8"))
        return execute(location("./node_modules/jslint/bin/jslint.js {0}".format(f.name)))
