#!/usr/bin/python3
""" Index module """
from api.v1.views import app_views
from flask import jsonify
from models import storage

statsDict = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', strict_slashes=False)
def ok_status():
    """ API status """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def obj_stats():
    """ Endpoint that retrieves the number of each objects by type """
    dict_stats = {}
    for key, value in statsDict.items():
        dict_stats[key] = storage.count(value)
    return jsonify(dict_stats)

if __name__ == "__main__":
    pass
