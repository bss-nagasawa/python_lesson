# test_imports.py

def test_flask_imports():
	try:
		from flask import Flask, request, render_template, redirect, url_for
		assert True
	except ImportError:
		assert False, "Flask関連のモジュールがインポートできません。"

def test_sqlite3_import():
	try:
		import sqlite3
		assert True
	except ImportError:
		assert False, "sqlite3モジュールがインポートできません。"

def test_requests_import():
	try:
		import requests
		assert True
	except ImportError:
		assert False, "requestsモジュールがインポートできません。"