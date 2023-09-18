#!/usr/bin/python3
"""Script that starts a Flask web"""
from flask import Flask, render_template
from models import storage


app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_route():
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hi_route():
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    text = text.replace("_", " ")
    return f'C {text}'


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_route(text="is_cool"):
    text = text.replace("_", " ")
    return f'Python {text}'


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    if isinstance(n, int):
        return f'{n} is a number'


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template_route(n):
    if isinstance(n, int):
        return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_route(n):
    if isinstance(n, int):
        odd_or_even = "even" if n % 2 == 0 else "odd"
        return render_template('6-number_odd_or_even.html', number=n,
                               odd_even=odd_or_even)

@app.route('/states_list', strict_slashes=False)
def html_route():
    "Display a list of all State objects sorted by name"
    states = storage.all().values("States")
    return render_template('7-states_list.html', states=states)

@app.teardown_appcontext
def close_route(exception):
    "Close the SQLAlchemy Session"
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
