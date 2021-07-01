from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Table, Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship, backref, session, query
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    total_balance = db.Column(db.Float)  # Total do usuário
    flutuation_bal = db.Column(db.Float)  # Total de lucro ou prejuízo

    # Um usuário tem várias criptos e transações:
    transactions = db.relationship('Transaction')
    criptos = db.relationship('Cripto')


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(150))
    nome_cripto = db.Column(db.String(150))
    quant = db.Column(db.Float)
    data = db.Column(db.String(150))
    quotation = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    cripto = db.relationship("Cripto", back_populates="transaction", uselist=False)

    def mostrar(self):
        tipo_maiuscula = self.tipo.upper()
        transacao_string = f'{tipo_maiuscula} || {self.quant} {self.nome_cripto} || {self.data} || ' \
                           f'{self.data} || {self.quotation} USD'
        return transacao_string


class Cripto(db.Model):
    __tablename__ = 'cripto'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), unique=True)
    total_balance = db.Column(db.Float)
    quotation = db.Column(db.Float)
    flutuation = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    transaction_id = db.Column(db.Integer, db.ForeignKey("transaction.id"))
    transaction = db.relationship("Transaction", back_populates="cripto")
