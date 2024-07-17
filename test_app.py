# モジュールインポートの確認
import pytest

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

@pytest.mark.imports
def test_requests_import():
	try:
		import requests
		assert True
	except ImportError:
		assert False, "requestsモジュールがインポートできません。"

# モジュールインポートの確認.END
#_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

# get_location_info()関数のテスト
from unittest.mock import patch
from app import get_location_info

# 成功した場合のテスト
# 正常系
@pytest.mark.parametrize("address, expected", [
    ("東京タワー", ("東京タワー, 4 Chome-2-8 Shibakoen, Minato City, Tokyo 105-0011, Japan", 35.6585805, 139.7454329)),
])
def test_get_location_info_normal(address, expected):
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            "status": "OK",
            "results": [{
                "formatted_address": expected[0],
                "geometry": {
                    "location": {
                        "lat": expected[1],
                        "lng": expected[2]
                    }
                }
            }]
        }
        assert get_location_info(address) == expected

# 異常系
@pytest.mark.parametrize("address", [
    ("東京タワー"),
])
def test_get_location_info_abnormal(address):
    with patch('requests.get') as mock_get:
        # 空の結果を返すが、期待されるキー構造を保持
        mock_get.return_value.json.return_value = {
            "status": "OK",
            "results": [{
                "formatted_address": None,  # formatted_address を None として設定
                "geometry": {
                    "location": {
                        "lat": None,
                        "lng": None
                    }
                }
            }]
        }
        assert get_location_info(address) == (None, None, None)

# 準正常系
@pytest.mark.parametrize("address, expected", [
    ("北極", ("North Pole", 90.0, 135.0)),  # 極端に大きい緯度
    ("南極", ("South Pole", -90.0, -135.0)),  # 極端に小さい緯度
])
def test_get_location_info_semi_normal(address, expected):
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            "status": "OK",
            "results": [{
                "formatted_address": expected[0],
                "geometry": {
                    "location": {
                        "lat": expected[1],
                        "lng": expected[2]
                    }
                }
            }]
        }
        assert get_location_info(address) == expected

# 失敗した場合のテスト
@pytest.mark.parametrize("address", [
	("存在しない場所"),
])
def test_get_location_info_failure(address):
	with patch('requests.get') as mock_get:
		mock_get.return_value.json.return_value = {
			"status": "ZERO_RESULTS"
		}
		assert get_location_info(address) == (None, None, None)

# get_location_info()関数のテスト.END
#_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
