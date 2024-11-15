#!/usr/bin/env python3
""" Module of Users views API """
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Return:
      - list of all User objects JSON represented
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """

    if user_id is None:
        abort(404)

    if user_id == "me" and request.current_user is None:
        abort(404)

    if user_id == "me":
        return jsonify(request.current_user.to_json())

    user = User.get(user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - empty JSON is the User has been correctly deleted
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)

    user = User.get(user_id)
    if user is None:
        abort(404)

    user.remove()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    JSON body:
      - email
      - password
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 400 if it can't create the new User
    """
    request_json = request.get_json(slice=True)

    if not request_json:
        return make_response(jsonify({"error": "Wrong format"}), 400)

    email = request_json.get("email")
    password = request_json.get("password")

    if not email:
        return make_response(jsonify({"error": "email missing"}), 400)
    if not password:
        return make_response(jsonify({"error": "password missing"}), 400)

    try:
        user = User()
        user.email = email
        user.password = password
        user.first_name = request_json.get("first_name")
        user.last_name = request_json.get("last_name")
        user.save()

        return make_response(jsonify(user.to_json()), 201)
    except Exception as err:
        return make_response(
            jsonify({"error": f"Can't create User: {err}"}), 400
        )


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """ PUT /api/v1/users/:id
    Path parameter:
      - User ID
    JSON body:
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if it can't update the User
    """
    if user_id is None:
        abort(404)

    user = User.get(user_id)
    if user is None:
        abort(404)

    request_json = request.get_json(slice=True)
    if not request_json:
        return make_response(jsonify({"error": "Wrong format"}), 400)

    if request_json.get('first_name') is not None:
        user.first_name = request_json.get('first_name')
    if request_json.get('last_name') is not None:
        user.last_name = request_json.get('last_name')

    user.save()

    return make_response(jsonify(user.to_json()), 200)
