#!./venv/bin/python3
import os
import datetime
import time
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
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Customer %r %r>' % (self.id, self.name)


class Review(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    completion_date = db.Column(db.DateTime, nullable=False)
    department = db.Column(db.String(80), nullable=False)
    risk_category = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(65535))
    customer = db.Column(db.Integer, db.ForeignKey('customer.id'))

    def __repr__(self):
        return '<Review %r>' % self.id


@app.route('/')
def index():
    customers = Customer.query.all()
    return render_template("index.html", customers=customers)


@app.route('/customer/new', methods=['GET', 'POST'])
def add_customer():
    if request.method == "GET":
        return render_template("new_customer.html")
    new_customer = Customer(
        name=request.form['customer_name'],
        id=request.form['customer_id']
    )
    new_review = Review(
        completion_date=datetime.datetime.strptime(request.form['review_date'], '%Y-%m-%d').date(),
        department=request.form['review_department'],
        risk_category=request.form['review_risk'],
        note=request.form['review_notes'],
        customer=new_customer.id,
    )
    db.session.add(new_customer)
    db.session.add(new_review)
    db.session.commit()
    return redirect('/')
    

@app.route('/customer/<customer_id>', methods=["GET", "POST"])
def profile(customer_id):
    if request.method == "GET":
        customer = Customer.query.get(customer_id)
        reviews = Review.query.filter_by(customer=customer.id).all() 
        return render_template("customer.html", customer=customer, reviews=reviews)
    new_review = Review(
        completion_date=datetime.datetime.strptime(request.form['review_date'], '%Y-%m-%d').date(),
        department=request.form['review_department'],
        risk_category=request.form['review_risk'],
        note=request.form['review_notes'],
        customer=customer_id,
    )
    db.session.add(new_review)
    db.session.commit()
    return redirect('/customer/%s' % customer_id)

if __name__ == '__main__':
    db.create_all()
    app.run('0.0.0.0', port=5000, debug=True)
