from module import Module, module_locator
from util import load_js
from flask import request

import sqlite3
import json


class TestModule(Module):
	def __init__(self):
		super(TestModule, self).__init__()

	@staticmethod
	def _get_connection():
		conn = sqlite3.connect("testing.db")
		return conn

	@staticmethod
	def ping():
		return "pong"

	def get(self, _id):
		cursor = self._get_connection().cursor()
		if _id == "*":  # Wild Card
			return [{"id": row[0], "text": row[1]} for row in cursor.execute("SELECT id, text FROM notes")]
		else:
			return [{"id": row[0], "text": row[1]} for row in cursor.execute(
				"SELECT id, text FROM notes WHERE id = ?", int(_id))]

	def put(self):
		data = json.loads(request.data.decode("utf-8"))
		conn = self._get_connection()
		cursor = conn.cursor()
		cursor.execute("INSERT INTO notes(text) VALUES(?)", (data["text"],))
		conn.commit()
		return {"id": cursor.lastrowid}

	def delete(self, _id):
		conn = self._get_connection()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM notes WHERE id = ?", (_id,))
		conn.commit()
		return {"success": True}

	def get_identifier(self):
		return ["_id"]

	def get_controller(self):
		return load_js("controller.js", lambda *args: module_locator(self, *args))
