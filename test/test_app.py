# モジュールインポート
import pytest
import sys
import os
# テストファイルのあるディレクトリの絶対パスを取得
current_dir = os.path.dirname(os.path.abspath(__file__))
# ルートディレクトリのパスを取得（'test'ディレクトリの1つ上）
parent_dir = os.path.dirname(current_dir)
# Pythonのパスリストにルートディレクトリを追加
sys.path.append(parent_dir)

@pytest.mark.imports
def test_flask_imports():
	try:
		from flask import Flask, request, render_template, redirect, url_for
		assert True
	except ImportError:
		assert False, "Flask関連のモジュールがインポートできません。"

@pytest.mark.imports
def test_sqlite3_import():
	try:
		import sqlite3
		assert True
	except ImportError:
		assert False, "sqlite3モジュールがインポートできません。"

# モジュールインポートの確認.END
#_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
