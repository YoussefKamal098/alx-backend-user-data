#!/usr/bin/env python3
"""
Session Authentication API

This module defines two routes for handling user authentication sessions:
- `/auth_session/login`: A POST endpoint for logging in users via email and
    password.
- `/auth_session/logout`: A DELETE endpoint for logging out users by
    destroying their session.

Each endpoint performs session management tasks such as validating
credentials, creating or destroying sessions, and setting or clearing
session cookies.

Routes:
    - POST /auth_session/login: Authenticates a user, creates a session,
        and sets the session ID in a cookie.
    - DELETE /auth_session/logout: Logs out a user by destroying their
        session and clearing the session cookie.

Functions:
    login: Handles the user login process by validating email and password,
        creating a session, and setting a session ID in a cookie.
    logout: Handles user logout by destroying the user's session and
        clearing the session cookie.
"""

import flask
from flask import jsonify, request, make_response, abort
from api.v1.views import app_views
from api.v1.auth.session_auth import SessionAuthInterface
from models.user import User
from config import config


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
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
    auth: SessionAuthInterface = flask.current_app.auth

    # Ensure `auth` is an instance of `SessionAuthInterface`
    if not isinstance(auth, SessionAuthInterface):
        return make_response(
            jsonify({"error": "Session management is not supported"}), 501
        )

    # Check if the user is already logged in
    session_id = request.cookies.get(config.SESSION_NAME)
    if session_id and auth.user_id_for_session_id(session_id):
        return make_response(
            jsonify({"error": "User already logged in"}), 400
        )

    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return make_response(jsonify({"error": "email missing"}), 400)

    if not password:
        return make_response(jsonify({"error": "password missing"}), 400)

    # Retrieve the User instance based on the email
    users = User.search({"email": email})
    user: User = users.first()

    if not user:
        return make_response(
            jsonify({"error": "no user found for this email"}), 404
        )

    # Check the password
    if not user.is_valid_password(password):
        return make_response(jsonify({"error": "wrong password"}), 401)

    # Create a session for the user
    session_id = auth.create_session(user.id)

    # Prepare the response with user details
    response = make_response(jsonify(user.to_json()))

    # Set the session ID in a cookie
    response.set_cookie(config.SESSION_NAME, session_id)

    return response


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False
)
def session_logout() -> str:
    """
    Handle user logout by destroying their session.

    Returns:
        flask.Response: A JSON response with an empty dictionary and
            status 200 if the session is destroyed, or 404 otherwise.
    """
    auth: SessionAuthInterface = flask.current_app.auth

    # Ensure `auth` is an instance of `SessionAuthInterface`
    if not isinstance(auth, SessionAuthInterface):
        return make_response(
            jsonify({"error": "Session management is not supported"}), 501
        )

    # Check if the user is logged in
    session_id = request.cookies.get(config.SESSION_NAME)
    if not session_id or not auth.user_id_for_session_id(session_id):
        return make_response(
            jsonify({"error": "No active session found"}), 404
        )

    if not auth.destroy_session(request):
        abort(404)

    return make_response(jsonify({}), 200)
