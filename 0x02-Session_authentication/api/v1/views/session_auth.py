#!/usr/bin/env python3
"""
Session auth API
"""
import flask
from flask import jsonify, request, make_response
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Handles user login by authenticating with email and password.

    This function processes a POST request at the route
    `/api/v1/auth_session/login`. It retrieves the user's email and
    password from the form data, validates the
    credentials, and, if the authentication is successful,
    creates a session for the user. The session ID is stored in
    a cookie to persist the session across requests.

    If the email or password is missing, the function
    aborts with an appropriate error
    message. If the user is not found or the password is incorrect,
    it returns a 404 or 401 status code respectively.

    Returns:
       flask.Response: A JSON response containing the user data
            and the session ID set in a cookie, or an error response
            with the corresponding HTTP status code.

    Raises:
       400: If either the email or password is missing.
       404: If no user is found for the provided email.
       401: If the password does not match the user's stored password.
   """
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
    session_name = flask.current_app.config['SESSION_NAME']
    response.set_cookie(session_name, session_id)

    return response
