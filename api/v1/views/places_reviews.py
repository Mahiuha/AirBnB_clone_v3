#!/usr/bin/python3
""" Review API actions """
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from flask import Flask, jsonify, make_response, request, abort


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_review(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get(Place, place_id)
    l_rev = []
    if not place:
        abort(404)
    for review in place.review:
        l_rev.append(review.to_dict())
    return jsonify(l_rev)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_reviews():
    """ Retrieves a Review object """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Place object """
    reviews = storage.all(Review, review_id)
    if reviews is None:
        abort(404)
    else:
        storage.delete(reviews)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review():
    """ Creates a Place """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        return "Not a JSON", 400
    request = request.json
    if "user_id" not in request:
        return "Missing user_id", 400
    user = storage.get(User, request['user_id'])
    if not user:
        abort(404)
    if "text" not in request:
        return "Missing name", 400
    request['place_id'] = place_id
    new_rev = Review(**request)
    new_rev.save()
    return jsonify(new_rev.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.json:
        return "Not a JSON", 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at',
                       'place_id', 'user_id']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
