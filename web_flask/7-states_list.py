#!/usr/bin/python3
"""Script that starts a Flask web"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)

@app.teardown_appcontext
def close_route(exception):
    "Close the SQLAlchemy Session"
    storage.close()


@app.route('/states_list', strict_slashes=False)
def html_route():
    "Display a list of all State objects sorted by name"
    states = storage.all(States).values()
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
