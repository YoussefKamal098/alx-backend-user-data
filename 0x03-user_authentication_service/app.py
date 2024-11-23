#!/usr/bin/env python3
"""
Simple Flask app with a single GET route returning a JSON message.
"""
from flask import Flask, jsonify, request

from auth import Auth

# Initialize Flask app
app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def home():
    """Return a JSON response with a message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """
    Register a new user.

    This endpoint expects 'email' and 'password' as form data. If the
    email is not already registered, it creates the user and returns
    a success message. If the email is already registered, it returns
    an error message with a 400 status code.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


# Run the app on host 0.0.0.0 and port 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
