#!/usr/bin/python3
""" Amenity API actions """
from api.v1.views import app_views
from flask import Flask, make_response, jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenity():
    """ Retrieves the list of all Amenity objects """
    amenities = storage.all(Amenity)
    l_ame = []
    for amenity in amenities.values():
        l_ame.append(amenities.to_dict())
    return jsonify(l_ame)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a City object """
    amenities = storage.all(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    else:
        storage.delete(amenities)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates an Amenity """
    if not request.json:
        return "Not a JSON", 400
    request = request.json
    if "name" not in request:
        return "Missing name", 400
    new_amenity = Amenity(**request)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.json:
        return "Not a JSON", 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
