from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.String(50), nullable=False)
    screen = db.Column(db.String(50), nullable=False)
    chip = db.Column(db.String(50), nullable=False)
    camera = db.Column(db.String(50), nullable=False)
