#!/usr/bin/python3
''' Places API actions'''
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import Flask, jsonify, make_response, request, abort


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_place():
    """ Retrieves the list of all Place objects of a City """
    city = storage.get(City, city_id)
    l_pla = []
    if not city:
        abort(404)
    for place in city.places:
        l_pla.append(place.to_dict())
    return jsonify(l_pla)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place():
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    places = storage.all(Place, place_id)
    if places is None:
        abort(404)
    else:
        storage.delete(places)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place():
    """ Creates a Place """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        return "Not a JSON", 400
    request = request.json
    if "user_id" not in request:
        return "Missing user_id", 400
    user = storage.get(User, request['user_id'])
    if not user:
        abort(404)
    if "name" not in request:
        return "Missing name", 400
    request['city_id'] = city_id
    new_place = Place(**request)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        return "Not a JSON", 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at', 'place_id']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
