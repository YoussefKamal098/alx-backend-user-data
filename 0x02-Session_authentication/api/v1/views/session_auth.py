#!/usr/bin/env python3
"""
Session auth API
"""
import os
from flask import jsonify, request, make_response
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Handles user login by authenticating with email and password.

    Processes a POST request at the route `/api/v1/auth_session/login`.
    Validates user credentials, creates a session, and sets the session ID
    in a cookie.

    Returns:
       flask.Response: A JSON response containing the user data
       and the session ID set in a cookie, or an error response
       with the corresponding HTTP status code.
    """
    from api.v1.app import auth

    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return make_response(jsonify({"error": "email missing"}), 400)

    if not password:
        return make_response(jsonify({"error": "password missing"}), 400)

    # Retrieve the User instance based on the email
    users = User.search({"email": email})
    if not users:
        return make_response(
            jsonify({"error": "no user found for this email"}), 404
        )

    user: User = users[0]

    # Check the password
    if not user.is_valid_password(password):
        return make_response(jsonify({"error": "wrong password"}), 401)

    # Create a session for the user
    session_id = auth.create_session(user.id)

    # Prepare the response with user details
    response = make_response(jsonify(user.to_json()))

    # Set the session ID in a cookie
    session_name = os.getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)

    return response
