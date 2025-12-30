from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask import Flask, request, jsonify
from database import get_db_connection
import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps
load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
@app.route("/")
def home():
    return "Secure Auth Backend Working 🔒"

# -------------------- REGISTER USER --------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, password_hash.decode("utf-8"))
        )
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------- LOGIN USER (returns JWT token) --------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()

        if not result:
            return jsonify({"message": "User does not exist"}), 404

        stored_hash = result[0]

        if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            token = jwt.encode(
                {
                    "email": email,
                    "exp": datetime.utcnow() + timedelta(hours=1)
                },
                app.config["SECRET_KEY"],
                algorithm="HS256"
            )
            return jsonify({"token": token}), 200
        else:
            return jsonify({"message": "Invalid password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------ CHECK TOKEN (middleware) ------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token missing"}), 401

        try:
            jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated


# -------------------- PROTECTED ROUTE --------------------
@app.route("/dashboard", methods=["GET"])
@token_required
def dashboard():
    return jsonify({"message": "Welcome to your dashboard 🔐"}), 200

@app.route("/profile", methods=["GET"])
def profile():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"}), 401

    try:
        decoded = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        email = decoded["email"]
        # Later you can also fetch more from DB using this email if you want
        return jsonify({"email": email}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == "__main__":
    app.run(debug=True)
