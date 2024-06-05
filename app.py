from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('bookings.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_week_dates():
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())  # Get the latest Monday
    return [(start_of_week + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(5)]

@app.route('/')
def index():
    week_dates = get_week_dates()
    timeslots = ['09:00 AM', '10:00 AM', '11:00 AM', '01:00 PM', '02:00 PM', '03:00 PM']
    
    conn = get_db_connection()
    bookings = conn.execute('SELECT day, slot, name FROM bookings').fetchall()
    conn.close()
    
    booking_data = {(row['day'], row['slot']): row['name'] for row in bookings}
    
    return render_template('index.html', week_dates=week_dates, timeslots=timeslots, booking_data=booking_data)

@app.route('/book', methods=['POST'])
def book():
    day = request.form['day']
    slot = request.form['slot']
    name = request.form['name']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO bookings (day, slot, name) VALUES (?, ?, ?)', (day, slot, name))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Booking confirmed!'})

if __name__ == "__main__":
    app.run(debug=True)
