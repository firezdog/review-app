import os
from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(
    os.path.join(project_dir, "customerdatabase.db")
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)


class Customer(db.Model):
    name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return '<Customer %r %r>' % (self.id, self.name)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        context = {}
        customers = Customer.query.all()
        return render_template("index.html", customers=customers)
    else:
        new_customer = Customer(
            name=request.form['customer_name'], id=request.form['customer_id'])
        db.session.add(new_customer)
        db.session.commit()
        return redirect('/')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
