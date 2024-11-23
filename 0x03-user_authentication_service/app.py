#!/usr/bin/env python3
"""
Simple Flask app with a single GET route returning a JSON message.
"""
from flask import Flask, jsonify, request, abort, make_response, redirect

from auth import Auth

# Initialize Flask app
app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """Return a JSON response with a message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
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


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """
    Handles user login by validating email and password.
    If valid, creates a session ID, sets it as a cookie,
    and returns a success response.

    Returns:
        JSON response with email and message if successful.
        Aborts with 401 status code if login credentials are invalid.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        abort(401)

    # Validate login credentials
    if not AUTH.valid_login(email, password):
        abort(401)

    # Create session and set session_id cookie
    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)

    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    Handles user logout by destroying the session based on
    the session_id cookie. Redirects to the homepage if successful,
    returns a 403 if the session is invalid.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)  # Forbidden if no session_id

    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")  # Redirect to the homepage after logout

    # If no valid user found, respond with 403 Forbidden
    abort(403)


@app.route("/profile", methods=["GET"])
def profile():
    """
    Handles the profile route by returning the user's email based on
    the session_id cookie. Responds with 403 if the session is invalid
    or the user does not exist.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)  # Forbidden if no session_id

    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email})

    # If no valid user found, respond with 403 Forbidden
    abort(403)


@app.route('/reset_password', methods=['POST'])
def reset_password():
    """
    Handles the POST request to reset the password.
    Takes the user's email and generates a reset token.
    """
    email = request.form.get('email')
    if not email:
        abort(400, description="Email is required")

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({
            "email": email,
            "reset_token": reset_token
        }), 200
    except ValueError:
        # If the user is not found, respond with a 403 Forbidden error
        abort(403, description="Email not registered")


# Run the app on host 0.0.0.0 and port 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
