from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

def get_db_connection():
    database = '/opt/telegram_bot/bookings.db'
    conn = sqlite3.connect(f"sqlite:///{database}")
    conn.row_factory = sqlite3.Row
    return conn

def get_week_dates():
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())  # Get the latest Monday
    return [(start_of_week + timedelta(days=i)).strftime('%Y-%B-%d') for i in range(5)]

@app.route('/')
def index():
    week_dates = get_week_dates()
    timeslots = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00']
    
    conn = get_db_connection()
    bookings = conn.execute('SELECT day, slot, name FROM booking').fetchall()
    conn.close()
    
    booking_data = {(row['day'], row['slot']): row['name'] for row in bookings}
    
    return render_template('index.html', week_dates=week_dates, timeslots=timeslots, booking_data=booking_data)

@app.route('/book', methods=['POST'])
def book():
    day = request.form['day']
    slot = request.form['slot']
    name = request.form['name']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO booking (day, slot, name) VALUES (?, ?, ?)', (day, slot, name))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Booking confirmed!'})

if __name__ == "__main__":
    app.run(debug=True)
