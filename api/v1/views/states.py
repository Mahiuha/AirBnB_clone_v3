#!/usr/bin/python3
""" State API actions """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """ Retrieves the list of all State objects """
    state_all = []
    for state in storage.all("State").values():
        state_all.append(state.to_dict())
    return jsonify(state_all)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """ Retrieves a State object """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """ Deletes a State object """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a State """
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})
    if "name" not in request.json:
        abort(400)
        return jsonify({"error": "Missing name"})
    new_state = State(**request.get_json())
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """ Updates a State object """
    lo_js = storage.get("State", state_id)
    if lo_js is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(lo_js, key, value)
    lo_js.save()
    return jsonify(lo_js.to_dict())
