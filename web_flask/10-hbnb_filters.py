#!/usr/bin/python3
"""Script that starts a Flask web"""
from flask import Flask, render_template
from models import storage
from models import *


app = Flask(__name__)


@app.teardown_appcontext
def close_route(err):
    "Close the SQLAlchemy Session"
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def filter_route():
    "Display a list of all  sorted by name"
    states = storage.all(States).values()
    amenities = storage.all(Amenity).values()
    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
