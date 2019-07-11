import sqlite3
from flask import Flask, render_template, g, request, jsonify
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        return jsonify(request.form)


if __name__ == '__main__':
    app.run(debug=True)
