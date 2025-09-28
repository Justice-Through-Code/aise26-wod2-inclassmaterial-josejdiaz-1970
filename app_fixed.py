# secure_flask_api.py
from flask import Flask, request, jsonify
import sqlite3
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import logging

# Load .env (if present)
load_dotenv()

# Basic configuration
DATABASE_URL = os.getenv("DATABASE_URL", "users.db")   # avoids embedding a full DB URL in code
API_SECRET = os.getenv("API_KEY")                     # must be set in environment or .env
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"

app = Flask(__name__)

# Configure logging (don't log sensitive data!)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Return a sqlite3 connection using a context manager style."""
    conn = sqlite3.connect(DATABASE_URL, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/health')
def health_check():
    """
    Health check: test DB reachability but do NOT return secrets or connection strings.
    """
    try:
        with get_db_connection() as conn:
            # quick lightweight operation to verify DB
            conn.execute("SELECT 1").fetchone()
        return jsonify({"status": "healthy"}), 200
    except Exception as e:
        logger.exception("Health check failed")
        return jsonify({"status": "unhealthy", "error": "database unavailable"}), 500

@app.route('/users', methods=['GET'])
def get_users():
    """
    Publicly listing users is often a privacy/security concern.
    Keep it for classroom/demo purposes but return only non-sensitive fields.
    In production you'd likely protect or remove this endpoint.
    """
    try:
        with get_db_connection() as conn:
            rows = conn.execute('SELECT id, username FROM users').fetchall()
        users = [{"id": r["id"], "username": r["username"]} for r in rows]
        return jsonify({"users": users})
    except Exception:
        logger.exception("Failed to fetch users")
        return jsonify({"message": "Failed to fetch users"}), 500

@app.route('/users', methods=['POST'])
def create_user():
    """
    Creates a user. Uses parameterized queries and a secure password hash.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "Invalid JSON"}), 400

    username = data.get('username', '').strip()
    password = data.get('password', '')

    # Basic validation
    if not username or not password:
        return jsonify({"message": "username and password are required"}), 400
    if len(password) < 8:
        return jsonify({"message": "password must be at least 8 characters"}), 400

    # Securely hash the password (werkzeug uses a salted KDF) ChatGPT Sept 2025. I didnt know about werkzeug.
    hashed_password = generate_password_hash(password)  # default: pbkdf2:sha256

    try:
        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
    except sqlite3.IntegrityError:
        # username UNIQUE constraint violation
        return jsonify({"message": "username already exists"}), 409
    except Exception:
        logger.exception("Failed to create user")
        return jsonify({"message": "Failed to create user"}), 500

    # Do NOT log sensitive info like plaintext passwords.
    logger.info("Created user: %s", username)
    return jsonify({"message": "User created", "username": username}), 201

@app.route('/login', methods=['POST'])
def login():
    """
    Authenticates a user using secure hash comparison.
    Does NOT leak whether username or password is wrong specifically.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"message": "Invalid JSON"}), 400

    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({"message": "username and password are required"}), 400

    try:
        with get_db_connection() as conn:
            row = conn.execute(
                "SELECT id, username, password FROM users WHERE username = ?",
                (username,)
            ).fetchone()
    except Exception:
        logger.exception("DB error during login")
        return jsonify({"message": "Login failed"}), 500

#CHATGPT Sept 2025
    if row and check_password_hash(row["password"], password):
        # In production, return a session token or JWT; do not return plaintext secrets.
        user_id = row["id"]
        logger.info("User %s (id=%s) logged in", username, user_id)
        return jsonify({"message": "Login successful", "user_id": user_id})
    else:
        # Generic error message to avoid username enumeration
        return jsonify({"message": "Invalid credentials"}), 401

def init_db():
    
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

if __name__ == '__main__':
    init_db()
    # Do not run with debug=True in production. Control via environment variable.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=FLASK_DEBUG)
