from flask import render_template, session
import sqlite3

def locations():
	# データベースに接続
	conn = sqlite3.connect('location.db')
	cursor = conn.cursor()

	# 現在のユーザーIDを取得
	user_id = session.get('user_id')

	# locationsテーブルから全てのカラムのデータを取得
	cursor.execute("SELECT * FROM locations WHERE user_id = ?", (user_id,))
	user_rows = cursor.fetchall()

	cursor.execute("SELECT * FROM locations WHERE user_id != ? OR user_id IS NULL", (user_id,))
	other_rows = cursor.fetchall()

	# データベース接続を閉じる
	conn.close()

	# 取得したデータをlocations.htmlテンプレートに渡す
	return render_template('locations.html', user_rows=user_rows, other_rows=other_rows)
