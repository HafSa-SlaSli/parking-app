from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

TOTAL_SPOTS = 10

def get_connection():
    conn = sqlite3.connect("parking.db")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cars(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate TEXT,
        entry_time TEXT
    )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def index():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cars")
    cars = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM cars")
    count = cursor.fetchone()[0]

    conn.close()

    free_spots = TOTAL_SPOTS - count

    return render_template("index.html", cars=cars, free=free_spots)

@app.route("/add", methods=["POST"])
def add_car():

    plate = request.form["plate"]
    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO cars (plate, entry_time) VALUES (?,?)",
        (plate, entry_time)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/exit/<int:id>")
def exit_car(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT entry_time FROM cars WHERE id=?", (id,))
    entry = cursor.fetchone()[0]

    entry = datetime.strptime(entry, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()

    hours = (now - entry).seconds / 3600
    price = round(hours * 2, 2)

    cursor.execute("DELETE FROM cars WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return f"Car exited. Price: {price} $"

if __name__ == "__main__":
    init_db()
    app.run(debug=True)