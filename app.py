from flask import Flask, request, render_template, redirect, url_for
from app.get_location import get_location_info
from app.locations import locations
from app.location_routes import location_bp
import sqlite3
import os

app = Flask(__name__)

app.add_url_rule('/locations', 'locations', locations)
app.register_blueprint(location_bp)

def get_db_connection():
    conn = sqlite3.connect('location.db')
    conn.row_factory = sqlite3.Row
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

if __name__ == '__main__':
	app.run(debug=True)
