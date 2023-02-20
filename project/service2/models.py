from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from service2.app import db

class Firm(db.Model):
    __tablename__ = 'firms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    auto_markets = db.relationship('AutoMarket', backref='firm', lazy=True)

    def __repr__(self):
        return f"Firm(name='{self.name}')"


class AutoMarket(db.Model):
    __tablename__ = 'auto_markets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    firm_id = db.Column(db.Integer, db.ForeignKey('firms.id'), nullable=False)
    cars = db.relationship('Car', backref='auto_market', lazy=True)

    def __repr__(self):
        return f"AutoMarket(name='{self.name}')"


class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    number = db.Column(db.String(80), unique=True, nullable=False)
    auto_market_id = db.Column(db.Integer, db.ForeignKey('auto_markets.id'), nullable=False)

    def __repr__(self):
        return f"Car(name='{self.name}', number='{self.number}')"