from flask import render_template
import sqlite3

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
