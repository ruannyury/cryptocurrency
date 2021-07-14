from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.orm import session, query
from sqlalchemy import desc
from website.models import User, Cripto, Transaction
from . import db
import json
import cryptocompare

views = Blueprint('views', __name__)


def lista_transacoes():
    # user = Transaction.query.filter_by(user_id=current_user.id).all()
    transacoes_user = Transaction.query.order_by(Transaction.id.desc()).all()
    return transacoes_user


def total_balance():
    soma_total = 0
    print(current_user.transactions)
    for trans in current_user.transactions:
        balance_day = trans.quotation * trans.quant

        if trans.tipo == 'compra':
            soma_total += balance_day
        elif trans.tipo == 'venda' or trans.tipo == 'transferencia':
            soma_total -= balance_day
    return soma_total


@views.route('/apenascripto', methods=['GET', 'POST'])
@login_required
def apenascripto():

    if request.method == 'POST':

        lista_de_siglas_cripto = listar()
        cripto_form = request.form.get('cripto').upper()

        if cripto_form not in lista_de_siglas_cripto:
            flash('Essa sigla não existe!', category='error')
            return redirect(url_for('views.apenascripto', user=current_user))  # Se não existir, reinicia a página
        elif request.form.get('voltar'):
            return redirect(url_for('views.home', user=current_user))
        else:
            flash('Listado!')
            return render_template('apenascripto.html', user=current_user, cripto=cripto_form)
    return render_template("apenascripto.html", user=current_user)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    total = f'Total em dólares: {total_balance()} USD.'
    flash(total)

    if request.method == 'POST':
        return redirect(url_for('views.apenascripto'))

    return render_template("home.html", user=current_user)


def listar():
    # Primeiro cria um dicionário com sigla e respectivo nome: {...'BTC': 'Bitcoin', 'NANO': 'Nano'...}
    dict_criptos_completo = cryptocompare.get_coin_list(format=False)
    dict_criptos = {}
    for sigla, nome in dict_criptos_completo.items():
        dict_criptos[sigla] = nome['CoinName']

    # Agora retirar apenas a sigla do dicionário acima
    lista_criptos = []
    for _sigla, _nome in dict_criptos.items():
        lista_criptos.append(_sigla)

    return lista_criptos


# PÁGINA PARA ADICIONAR TRANSAÇÃO
@views.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        transaction_form = request.form.get('transaction')  # Recebe a resposta do tipo da transação
        # Verifica se a sigla que o usuário colocou existe:
        # Pra isso, usa-se a função listar() que retorna uma lista contendo todas as siglas cripto:
        lista_de_siglas_cripto = listar()
        cripto_form = request.form.get('cripto').upper()

        if cripto_form not in lista_de_siglas_cripto:
            flash('Essa sigla não existe!')
            return redirect(url_for('auth.editportfolio', user=current_user))  # Se não existir, reinicia a página
        else:
            pass

        transaction_quant = request.form.get('quant')
        transaction_data = request.form.get('data')  # Recebe a data da transação
        flash('Transação adicionada!')  # Printa a data apenas para testar e ver como o formato fica em string

        transaction_quotation = request.form.get('cotacao')  # Adiciona a cotação daquela moeda no objeto

        new_transaction = Transaction(tipo=transaction_form,
                                      nome_cripto=cripto_form,
                                      quant=transaction_quant,
                                      data=transaction_data,
                                      quotation=transaction_quotation,
                                      user_id=current_user.id)

        # transactions = new_transaction.order_by(new_transaction.id.desc()).all()
        # flash(transactions)

        db.session.add(new_transaction)
        db.session.commit()

        return redirect(url_for('views.home'))

    return render_template("editportfolio.html", user=current_user)


@views.route('/delete-trans', methods=['POST'])
def delete_trans():
    trans = json.loads(request.data)
    trans_id = trans['transId']
    trans = Transaction.query.get(trans_id)
    if trans:
        if trans.user_id == current_user.id:
            db.session.delete(trans)
            db.session.commit()

    return jsonify({})
