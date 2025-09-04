import mysql.connector
from flask import Flask, render_template
import psutil
import datetime

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "sysmon",
    "password": "password123",
    "database": "sysmon",
    "ssl_disabled": True
}


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp VARCHAR(50),
            cpu FLOAT,
            ram FLOAT,
            uptime VARCHAR(100),
            logs TEXT
        )
    """)
    conn.commit()
    conn.close()


def collect_metrics():
    uptime_seconds = int(datetime.datetime.now().timestamp() - psutil.boot_time())
    uptime_str = str(datetime.timedelta(seconds=uptime_seconds))
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    logs = "System running smoothly"
    return cpu, ram, uptime_str, logs


@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM metrics ORDER BY id DESC LIMIT 1")
    last = cur.fetchone()

    cur.execute("SELECT timestamp, cpu, ram FROM metrics ORDER BY id DESC LIMIT 24")
    history = cur.fetchall()

    conn.close()

    labels = [h[0] for h in history][::-1]
    cpu_data = [h[1] for h in history][::-1]
    ram_data = [h[2] for h in history][::-1]

    return render_template(
        "index.html",
        last=last,
        labels=labels,
        cpu_data=cpu_data,
        ram_data=ram_data,
    )


if __name__ == "__main__":
    init_db()

    # Запишем метрики при старте (для теста)
    conn = get_db()
    cur = conn.cursor()
    cpu, ram, uptime, logs = collect_metrics()
    cur.execute(
        "INSERT INTO metrics (timestamp, cpu, ram, uptime, logs) VALUES (%s, %s, %s, %s, %s)",
        (datetime.datetime.now().strftime("%H:%M"), cpu, ram, uptime, logs),
    )
    conn.commit()
    conn.close()

    app.run(debug=True)

