# Simple Python API - Starting Point for GitHub Classroom Assignment
# This code has intentional security flaws for educational purposes

from flask import Flask, request, jsonify
import sqlite3
import hashlib


app = Flask(__name__)

# Security Issue: Hardcoded secrets
DATABASE_URL = "postgresql://admin:password123@localhost/prod"
API_SECRET = "sk-live-1234567890abcdef"


def get_db_connection():
    return sqlite3.connect('users.db')

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "database": DATABASE_URL})

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT id, username FROM users').fetchall()
    conn.close()
    return jsonify({"users": [{"id": u[0], "username": u[1]} for u in users]})

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Security Issue: Weak password hashing
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    
    conn = get_db_connection()
    # Security Issue: SQL injection vulnerability
    conn.execute(
        f"INSERT INTO users (username, password) VALUES ('{username}', '{hashed_password}')"
    )
    conn.commit()
    conn.close()
    
    # Security Issue: Logging sensitive information
    print(f"Created user: {username} with password: {password}")
    return jsonify({"message": "User created", "username": username})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    
    conn = get_db_connection()
    # Security Issue: SQL injection vulnerability
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{hashed_password}'"
    user = conn.execute(query).fetchone()
    conn.close()
    
    if user:
        return jsonify({"message": "Login successful", "user_id": user[0]})
    return jsonify({"message": "Invalid credentials"}), 401

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)