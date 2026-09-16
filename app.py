
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


# =========================
# Database
# =========================

def init_db():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            water REAL,
            electricity REAL,
            carbon REAL
        )
    """)

    conn.commit()

    conn.close()


# =========================
# Home
# =========================

@app.route("/")
def home():

    return render_template("index.html")


# =========================
# Water Calculator
# =========================

@app.route("/calc")
def calc():

    return render_template("calculator.html")


# =========================
# Save Water
# =========================

@app.route("/save_water", methods=["POST"])
def save_water():

    water = request.form["water"]

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO usage_data (water) VALUES (?)",
        (water,)
    )

    conn.commit()

    conn.close()

    return "Water saved successfully"


# =========================
# Electricity Calculator
# =========================

@app.route("/electricity")
def electricity():

    return render_template("electricity.html")


# =========================
# Save Electricity
# =========================

@app.route("/save_electricity", methods=["POST"])
def save_electricity():

    electricity = request.form["electricity"]

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO usage_data (electricity) VALUES (?)",
        (electricity,)
    )

    conn.commit()

    conn.close()

    return "Electricity saved successfully"


# =========================
# Carbon Calculator
# =========================

@app.route("/carbon")
def carbon():

    return render_template("carbon.html")


# =========================
# Save Carbon
# =========================

@app.route("/save_carbon", methods=["POST"])
def save_carbon():

    carbon = request.form["carbon"]

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO usage_data (carbon) VALUES (?)",
        (carbon,)
    )

    conn.commit()

    conn.close()

    return "Carbon saved successfully"


# =========================
# Dashboard
# =========================

@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()


    # Latest Water

    cursor.execute("""
        SELECT water
        FROM usage_data
        WHERE water IS NOT NULL
        ORDER BY id DESC
        LIMIT 1
    """)

    water_result = cursor.fetchone()


    # Latest Electricity

    cursor.execute("""
        SELECT electricity
        FROM usage_data
        WHERE electricity IS NOT NULL
        ORDER BY id DESC
        LIMIT 1
    """)

    electricity_result = cursor.fetchone()


    # Latest Carbon

    cursor.execute("""
        SELECT carbon
        FROM usage_data
        WHERE carbon IS NOT NULL
        ORDER BY id DESC
        LIMIT 1
    """)

    carbon_result = cursor.fetchone()


    conn.close()


    # Water

    if water_result:

        water = water_result[0]

    else:

        water = 0


    # Electricity

    if electricity_result:

        electricity = electricity_result[0]

    else:

        electricity = 0


    # Carbon

    if carbon_result:

        carbon = carbon_result[0]

    else:

        carbon = 0


    return render_template(
        "dashboard.html",
        water=water,
        electricity=electricity,
        carbon=carbon
    )


# =========================
# Run Application
# =========================
# استدعاء الدالة مباشرة خارج الشرط لإنشاء قاعدة البيانات فوراً عند أي طريقة تشغيل
init_db()

if __name__ == "__main__":
    app.run(debug=True)