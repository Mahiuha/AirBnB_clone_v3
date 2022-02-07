#!/usr/bin/python3
"""
Objects that handles all default RestFul API actions:
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def retrieves_list(state_id):
    """ Retrieves the list of all City objects """
    request_state = storage.get("State", state_id)

    if request_state is None:
        abort(404)

    cities = request_state.cities
    request_city = []

    for city in cities:
        request_city.append(city.to_dict())
    return jsonify(request_city)


@app_views.route('/cities/<city_id>', methods=['GET'])
def retrieves_id(city_id):
    """ Retrieves City obj by Id """
    request_city = storage.get("City", city_id)

    if request_city is None:
        abort(404)
    return jsonify(request_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def deletes_city(city_id):
    """ Deletes a City obj """

    delete_id = storage.get("City", city_id)

    if delete_id is None:
        abort(404)

    else:
        delete_id.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def creates_city(state_id):
    """ Creates City """
    id_state = storage.get("State", state_id)

    if id_state is None:
        abort(404)

    new = request.get_json()

    if new is None:
        abort(404, {"Not a JSON"})

    if 'name' not in new:
        abort(404, {"Missing name"})

    new = City(name=request.json['name'], state_id=state_id)
    storage.new(new)
    storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def updates_cities(city_id):
    """ Updates a City obj """
    request_city = request.get_json()

    if request_city is None:
        abort(400, {"Not a JSON"})

    update = storage.get("City", city_id)

    if update is None:
        abort(404)

    for key in request_city:
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(update, key, request_city[key])
    storage.save()
    return jsonify(update.to_dict()), 200
