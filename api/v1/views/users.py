#!/usr/bin/python3
""" User API actions """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ Retrieves the list of all User objects """
    user_all = []
    for user in storage.all("User").values():
        user_all.append(user.to_dict())
    return jsonify(user_all)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes an User object """
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a User """
    if not request.json:
        return "Not a JSON", 400
    if "email" not in request.json:
        return "Missing email", 400
    if "password" not in request.json:
        return "Missing password", 400
    request = request.json
    new_user = User(**request)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates an User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.json:
        return "Not a JSON", 400
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
