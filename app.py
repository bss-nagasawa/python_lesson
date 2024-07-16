from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import requests

app = Flask(__name__)

def get_location_info(address):
    # Google Maps Geocoding APIのエンドポイント
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    # APIキー（あなたのAPIキーに置き換えてください）
    api_key = "AIzaSyB4MUe3ZTOSkkZwRYVlNUStuZ3tMKFFXsg"
    # パラメータの設定
    params = {
        "address": address,
        "key": api_key
    }
    # APIリクエストを送信
    response = requests.get(url, params=params)
    # レスポンスのJSONを解析
    data = response.json()
    # 緯度と経度を取得
    if data["status"] == "OK":
        formatted_address = data["results"][0]["formatted_address"]
        latitude = data["results"][0]["geometry"]["location"]["lat"]
        longitude = data["results"][0]["geometry"]["location"]["lng"]
        return formatted_address, latitude, longitude  # 修正: 実際の住所と緯度、経度をタプルとして返す
    else:
        return None, None, None  # 修正: 位置情報が取得できなかった場合

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None  # エラーメッセージ用の変数を初期化
    if request.method == 'POST':
        name = request.form['name']
        subname = request.form['subname']
        # 修正: 実際の住所も受け取るように変更
        address, latitude, longitude = get_location_info(name)

        if address is not None:
            # データベースに接続
            conn = sqlite3.connect('location.db')
            cursor = conn.cursor()
            # locationsテーブルにデータを挿入
            cursor.execute("INSERT INTO locations (name, address, subname, latitude, longitude) VALUES (?, ?, ?, ?, ?)", (name, address, subname, latitude, longitude))
            conn.commit()
            conn.close()

            # locationsページにリダイレクト
            return redirect(url_for('locations'))
        else:
            # 位置情報が取得できなかった場合のエラーメッセージ
            error_message = "指定された住所の位置情報を取得できませんでした。"

    # エラーメッセージを含めてテンプレートをレンダリング
    return render_template('index.html', error_message=error_message)

@app.route('/locations')
def locations():
	# データベースに接続
	conn = sqlite3.connect('location.db')
	cursor = conn.cursor()

	# locationsテーブルから全てのカラムのデータを取得
	cursor.execute("SELECT * FROM locations")
	rows = cursor.fetchall()

	# データベース接続を閉じる
	conn.close()

	# 取得したデータをlocations.htmlテンプレートに渡す
	return render_template('locations.html', rows=rows)

if __name__ == '__main__':
	app.run(debug=True)