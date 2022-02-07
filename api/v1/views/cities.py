#!/usr/bin/python3
""" City API actions """
from api.v1.views import app_views
from flask import Flask, make_response, jsonify, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_city_state(state_id):
    """ Retrieves the list of all City objects of a State """
    states = storage.get(State, state_id)
    l_city = []
    if not states:
        abort(404)
    for city in states.cities:
        l_city.append(city.to_dict())
    return jsonify(l_city)


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Retrieves a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    else:
        storage.delete(cities)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ Creates a State """
    if not request.json:
        return "Not a JSON", 400
    request = request.json
    if "name" not in request:
        return "Missing name", 400
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    request['state_id'] = state_id
    new_city = City(**request)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        return "Not a JSON", 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
