from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from website.models import Note, User, Cripto, Transaction
from . import db
import json
import cryptocompare

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

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
