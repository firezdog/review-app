import sqlite3
from flask import Flask, render_template, g, request, jsonify
app = Flask(__name__)

DATABASE = './database.db'


def get_db():
    db = getattr(g, '_database', None)
    if (db is None):
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        return jsonify(request.form)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
