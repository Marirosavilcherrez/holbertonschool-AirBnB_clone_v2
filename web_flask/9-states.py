#!/usr/bin/python3
"""Script that starts a Flask web"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)


@app.teardown_appcontext
def close_route(err):
    "Close the SQLAlchemy Session"
    storage.close()


@app.route('/states', strict_slashes=False)
def state_route():
    "Display a list of all State objects sorted by name"
    states = storage.all(States).values()
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def state_id_route():
    "Display a list of all State objects wiht id sorted by name"
    states = storage.all(States).values()
    cities = storage.all(Cities).values()
    return render_template('9-states.html', states=states, cities=cities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
