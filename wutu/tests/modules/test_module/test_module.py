from wutu.module import Module, module_locator
from wutu.util import load_js
from flask import request

import sqlite3
import json

class TestModule(Module):
    def __init__(self):
        super(TestModule, self).__init__()

    def _get_connection(self):
        conn = sqlite3.connect("testing.db")
        return conn

    def ping(self):
        return "pong"

    def get(self, id):
        cursor = self._get_connection().cursor()
        if id == "*": #Wild Card
            return [{"id": row[0], "text": row[1]} for row in cursor.execute("SELECT id, text FROM notes")]
        else:
            return [{"id": row[0], "text": row[1]} for row in cursor.execute("SELECT id, text FROM notes WHERE id = ?", int(id))]

    def put(self):
        data = json.loads(request.data.decode("utf-8"))
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes(text) VALUES(?)", (data["text"],))
        conn.commit()
        return {"id": cursor.lastrowid}

    def get_identifier(self):
        return ["id"]

    def get_controller(self):
        return load_js("controller.js", lambda *args: module_locator(self, *args))
