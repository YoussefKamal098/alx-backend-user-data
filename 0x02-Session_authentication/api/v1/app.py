#!/usr/bin/env python3
"""
Flask application for managing API requests with authentication.
Handles authentication using dynamic auth type based on AUTH_TYPE
environment variable. Includes error handling
for 400, 401, and 404 HTTP status codes.
"""
import flask
from flask import Flask, abort, request, jsonify
from flask_cors import CORS

from api.v1.views import app_views
from api.v1.auth.auth_factory_provider import DefaultAuthFactoryProvider
from api.v1.auth.auth import AuthInterface
from config import config

# Initialize Flask app and CORS
app = Flask(__name__)

app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize the factory provider
auth_factory_provider = DefaultAuthFactoryProvider()

# Get the factory based on the environment variable AUTH_TYPE
auth_factory = auth_factory_provider.get_factory(config.AUTH_TYPE)

# Create the corresponding Auth instance
app.auth = auth_factory.create_auth()

# Excluded paths for authentication
EXCLUDED_PATHS = [
    '/api/v1/status/',
    '/api/v1/auth_session/login/',
    '/api/v1/unauthorized/',
    '/api/v1/forbidden/'
]


@app.before_request
def handle_authentication() -> None:
    """Authentication and authorization before each request."""
    # Check if request path is excluded from authentication
    auth: AuthInterface = flask.current_app.auth

    if not auth or not auth.require_auth(request.path, EXCLUDED_PATHS):
        return

    # Check for both Authorization header and Session cookie
    if (not auth.authorization_header(request) and
            not auth.session_cookie(request)):
        abort(401)

    request.current_user = auth.current_user(request)
    if not request.current_user:
        abort(403)


@app.errorhandler(404)
def not_found(_error) -> str:
    """Handle 404 Not Found error."""
    response = jsonify({"error": "Not Found"})
    response.status_code = 404
    return response


@app.errorhandler(401)
def unauthorized(_error) -> str:
    """Handle 401 Unauthorized error."""
    response = jsonify({"error": "Unauthorized"})
    response.status_code = 401
    return response


@app.errorhandler(403)
def forbidden(_error) -> str:
    """Handle 403 Forbidden error."""
    response = jsonify({"error": "Forbidden"})
    response.status_code = 403
    return response


if __name__ == "__main__":
    app.run(host=config.API_HOST, port=config.API_PORT)
