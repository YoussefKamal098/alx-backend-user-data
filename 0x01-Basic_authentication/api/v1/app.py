#!/usr/bin/env python3
"""
API Route module
"""
import os
from flask import Flask, abort, request, jsonify, Response
from flask_cors import CORS
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

# Initialize Flask app and CORS
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

"""
Determine which authentication class to use based on
AUTH_TYPE environment variable
"""
auth_type = os.getenv('AUTH_TYPE')
auth = BasicAuth() if auth_type == 'basic_auth' else Auth()

# Excluded paths for authentication
EXCLUDED_PATHS = [
    '/api/v1/status/',
    '/api/v1/unauthorized/',
    '/api/v1/forbidden/'
]


@app.before_request
def handle_authentication() -> None:
    """Authentication and authorization before each request."""
    if not auth or not auth.require_auth(request.path, EXCLUDED_PATHS):
        return

    if not auth.authorization_header(request):
        abort(401)
    if not auth.current_user(request):
        abort(403)


@app.errorhandler(404)
def not_found(_error) -> Response:
    """Handle 404 Not Found error."""
    response = jsonify({"error": "Not Found"})
    response.status_code = 404
    return response


@app.errorhandler(401)
def unauthorized(_error) -> Response:
    """Handle 401 Unauthorized error."""
    response = jsonify({"error": "Unauthorized"})
    response.status_code = 401
    return response


@app.errorhandler(400)
def bad_request(error) -> Response:
    """Handle 400 Bad Request error."""
    response = jsonify({"error": error})
    response.status_code = 400
    return response


@app.errorhandler(403)
def forbidden(_error) -> Response:
    """Handle 403 Forbidden error."""
    response = jsonify({"error": "Forbidden"})
    response.status_code = 403
    return response


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    app.run(host=host, port=int(port))
