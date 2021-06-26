from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Table, Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    bitcoin_quant = db.Column(db.Float)
    ethereum_quant = db.Column(db.Float)
    nano_quant = db.Column(db.Float)
    bnb_quant = db.Column(db.Float)
    ada_quant = db.Column(db.Float)
    litecoin_quant = db.Column(db.Float)
    total_balance = db.Column(db.Float)  # Total do usuário
    flutuation_bal = db.Column(db.Float)  # Total de lucro ou prejuízo

    # Um usuário tem várias notas, criptos e transações:
    notes = db.relationship('Note')
    criptos = db.relationship('Cripto')
    transactions = db.relationship('Transaction')


class Note(db.Model):
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
    quotation = db.Column(db.Float)
    flutuation = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    transaction_id = db.Column(db.Integer, ForeignKey('Transaction.id'))


class Bitcoin(db.Model):
    __tablename__ = 'Bitcoin'

    id = db.Column(db.Integer, primary_key=True)
    quotation = db.Column(db.Float)  # Cotação do dia
    flutuation = db.Column(db.Float)  # Lucro ou prejuízo do Bitcoin apenas


class Ethereum(db.Model):
    __tablename__ = 'Ethereum'

    id = db.Column(db.Integer, primary_key=True)
    quotation = db.Column(db.Float)
    flutuation = db.Column(db.Float)


class Nano(db.Model):
    __tablename__ = 'Nano'

    id = db.Column(db.Integer, primary_key=True)
    quotation = db.Column(db.Float)
    flutuation = db.Column(db.Float)


class Bnb(db.Model):
    __tablename__ = 'Bnb'

    id = db.Column(db.Integer, primary_key=True)
    quotation = db.Column(db.Float)
    flutuation = db.Column(db.Float)


class Ada(db.Model):
    __tablename__ = 'Ada'

    id = db.Column(db.Integer, primary_key=True)
    quotation = db.Column(db.Float)
    flutuation = db.Column(db.Float)


class Litecoin(db.Model):
    __tablename__ = 'Litecoin'

    id = db.Column(db.Integer, primary_key=True)
    quotation = db.Column(db.Float)
    flutuation = db.Column(db.Float)
