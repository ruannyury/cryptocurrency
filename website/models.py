from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Table, Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    total_balance = db.Column(db.Float)  # Total do usuário
    # flutuation_bal = db.Column(db.Float)  # Total de lucro ou prejuízo

    # Um usuário tem várias notas, criptos e transações:
    notes = db.relationship('Note')
    criptos = db.relationship('Cripto')
    transactions = db.relationship('Transaction')


class Note(db.Model):
    __tablename__ = 'note'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Transaction(db.Model):
    __tablename__ = 'Transaction'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(150), unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    criptos = db.relationship("Cripto", uselist=False, backref="Transaction")


class Cripto(db.Model):
    __tablename__ = 'Cripto'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), unique=True)
    total_balance = db.Column(db.Float)
    quotation = db.Column(db.Float)
    flutuation = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    transaction_id = db.Column(db.Integer, ForeignKey('Transaction.id'))
