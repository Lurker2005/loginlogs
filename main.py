from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# -----------------------------
# DB CONNECTION FUNCTION
# -----------------------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_DB_PASSWORD",
        database="YOUR_DB_NAME"
    )

# -----------------------------
# API: STORE LOGIN DETAILS
# -----------------------------
@app.route("/log/user-login", methods=["POST"])
def log_user_login():
    try:
        data = request.json
        username = data.get("username")
        ip = data.get("ip")
        lat = data.get("lat")
        lng = data.get("long")
        device = data.get("device", "unknown")
        os_name = data.get("os", "unknown")

        db = get_db()
        cursor = db.cursor()

        sql = """
        INSERT INTO login_logs (username, ip_address, latitude, longitude, device, os)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (username, ip, lat, lng, device, os_name))
        db.commit()

        return jsonify({"status": "success", "message": "Login log stored"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6001, debug=True)
