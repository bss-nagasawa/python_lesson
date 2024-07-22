from flask import render_template, Blueprint
import sqlite3
import os

location_bp = Blueprint('location_bp', __name__)

@location_bp.route('/location/<int:id>')
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