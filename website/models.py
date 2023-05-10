from website import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(20))
    budget = db.Column(db.Integer(), nullable=False, default=1000)

class Products(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(30), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    barcode = db.Column(db.Integer, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    