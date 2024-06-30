from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
socketio = SocketIO(app)

def get_db_connection():
    database = 'bookings.db'
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    return conn

def get_week_dates():
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())  # Get the latest Monday
    return [(start_of_week + timedelta(days=i)).strftime('%Y-%B-%d') for i in range(5)]


def get_week_dates_and_weekdays():
    today = datetime.now()
    # Get the start of the current week (Monday)
    start_of_week = today - timedelta(days=today.weekday())
    if today.weekday() >= 5:
        start_of_week += timedelta(days=7)  # If today is Saturday or Sunday, get next Monday
    weekdays = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]
    return [(weekdays[i]) for i in range(5)]


@app.route('/')
def index():
    week_dates = get_week_dates_and_weekdays()
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
    
    booking = {'day': day, 'slot': slot, 'name': name}
    socketio.emit('update_bookings', booking)
    
    return jsonify({'status': 'success', 'message': 'Booking confirmed!'})

@socketio.on('connect')
def handle_connect():
    conn = get_db_connection()
    bookings = conn.execute('SELECT day, slot, name FROM booking').fetchall()
    conn.close()
    
    booking_data = {(row['day'], row['slot']): row['name'] for row in bookings}
    # Convert the keys to strings
    booking_data_str_keys = {f"{key[0]}_{key[1]}": value for key, value in booking_data.items()}
    
    emit('init_bookings', booking_data_str_keys)

if __name__ == "__main__":
    socketio.run(app, debug=True)
