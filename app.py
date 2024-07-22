from flask import Flask, request, render_template, redirect, url_for, session
from app.get_location import get_location_info
from app.locations import locations
from app.location_routes import location_bp
import sqlite3
import os

app = Flask(__name__)

app.add_url_rule('/locations', 'locations', locations)
app.register_blueprint(location_bp)

def get_db_connection():
    db_path = 'location.db'  # データベースファイルへのパスを適切に設定してください。
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        print("データベースに接続しました。")  # コンソールに出力
    except sqlite3.Error as e:
        print(f"データベース接続エラー: {e}")  # コンソールにエラーを出力
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    if request.method == 'POST':
        name = request.form['name']
        subname = request.form['subname']
        address, latitude, longitude = get_location_info(name)

        if address is not None:
            with get_db_connection() as conn:
                conn.execute("INSERT INTO locations (name, address, subname, latitude, longitude) VALUES (?, ?, ?, ?, ?)", (name, address, subname, latitude, longitude))
                conn.commit()
            return redirect(url_for('locations'))
        else:
            error_message = "指定された住所の位置情報を取得できませんでした。"
    return render_template('index.html', error_message=error_message)


@app.route('/location/<int:id>')
def location_detail(id):
    conn = sqlite3.connect('location.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM locations WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if row:
        return render_template('locationDetail.html', row=row, api_key=google_maps_api_key)
    else:
        return "Location not found", 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None  # メッセージの初期化
    if request.method == 'POST':
        user_mail = request.form['user_mail']
        user_pass = request.form['user_pass']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE user_mail = ?', (user_mail,)).fetchone()
        conn.close()

        # パスワードのハッシュ化を確認する代わりに、データベースのパスワードと直接比較
        if user is None or user['user_pass'] != user_pass:
            message = 'Invalid email or password'
            return render_template('login.html', message=message)  # 失敗メッセージを渡す
        else:
            session['user_id'] = user['user_id']
            message = 'Login successful'
            return redirect(url_for('locations', message=message))  # 成功メッセージを渡す

    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    # セッションからユーザーIDを削除
    session.pop('user_id', None)
    # ログインページにリダイレクト
    return redirect(url_for('login'))

# Flaskの秘密鍵を設定（セッション管理に必要）
app.secret_key = os.urandom(24)
@app.before_request
def require_login():
    allowed_routes = ['login', 'user_regist']
    if 'user_id' not in session and request.endpoint not in allowed_routes:
        return redirect(url_for('login'))

@app.route('/user_regist', methods=['GET', 'POST'])
def user_regist():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_mail = request.form['user_mail']
        user_pass = request.form['user_pass']

        conn = get_db_connection()
        conn.execute('INSERT INTO users (user_name, user_mail, user_pass) VALUES (?, ?, ?)', (user_name, user_mail, user_pass))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('user_regist.html')

if __name__ == '__main__':
	app.run(debug=True)
