from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Intentionally added for Bandit to detect
PASSWORD = "hardcoded_password_12345"  # This is a security issue!
API_KEY = "sk-1234567890abcdef"  # Another security issue!

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to DevSecOps Python Application",
        "status": "running",
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "flask-app"
    }), 200

@app.route('/api/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify({
            "message": "User created",
            "user": data.get('username', 'anonymous')
        }), 201
    else:
        return jsonify({
            "users": ["alice", "bob", "charlie"]
        }), 200

@app.route('/api/data')
def get_data():
    return jsonify({
        "data": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"}
        ]
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)