
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from service1.app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    nickname = db.Column(db.String(80), nullable=False)
    date_reg = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    cars = db.relationship('Car', backref='user', lazy=True)

    def __repr__(self):
        return f"User(email='{self.email}', nickname='{self.nickname}')"

class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    number = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Car(name='{self.name}', number='{self.number}')"

# ****