import requests
import os
from dotenv import load_dotenv

def get_location_info(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')  # 環境変数からAPIキーを取得
    params = {
        "address": address,
        "key": api_key
    }
    response = requests.get(url, params=params, timeout=10)  # タイムアウトを設定
    data = response.json()
    if data["status"] == "OK":
        formatted_address = data["results"][0]["formatted_address"]
        latitude = data["results"][0]["geometry"]["location"]["lat"]
        longitude = data["results"][0]["geometry"]["location"]["lng"]
        return formatted_address, latitude, longitude
    else:
        return None, None, None
