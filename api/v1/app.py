#!/usr/bin/python3
""" HNBN API """
from flask import Flask, Blueprint, jsonify, make_response, render_template
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_app(cd):
    """ Method to handle @app.teardown_appcontext """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ 404 handling """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host=host, port=int(port), threaded=True)
