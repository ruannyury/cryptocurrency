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
        transaction_form = request.form['transaction']  # Recebe a resposta do tipo da transação
        transaction_ = Transaction()
        # Verifica qual o tipo da transação e adiciona no atributo "tipo" do objeto transaction_
        if transaction_form == 1:
            transaction_.tipo = "venda"
        elif transaction_form == 2:
            transaction_.tipo = "compra"
        else:
            transaction_.tipo = "transferencia"
        # Verifica se a sigla que o usuário colocou existe:
        # Pra isso, usa-se a função listar() que retorna uma lista contendo todas as siglas cripto:
        lista_de_siglas_cripto = listar()
        if request.form['cripto'].upper() not in lista_de_siglas_cripto:
            flash('Essa sigla não existe!')
            return redirect(url_for('editportfolio.html', user=current_user))  # Se não existir, reinicia a página
        else:
            cripto_form = request.form['cripto'].upper()  # Se existir, a cripto é adicionada ao atributo "cripto"
            # do objeto transaction_
            transaction_.nome = cripto_form

        transaction_.data = request.form['data']  # Adiciona a data da transação ao objeto
        flash(transaction_.data)  # Printa a data apenas para testar e ver como o formato fica em string

        transaction_.quotation = request.form['cotacao']  # Adiciona a cotação daquela moeda no objeto

        return redirect(url_for('views.home'))

    return render_template("editportfolio.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
