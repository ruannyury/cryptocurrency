from flask import Flask, request, url_for, redirect, render_template, flash
from app.models.tables import Cliente, User
import cryptocompare


app = Flask(__name__)
app.config.from_object('config')

global_id = 4
global_codigo = 400


def atualizar_1(cliente):
    global global_id
    global global_codigo
    global_id += 1
    global_codigo += 100
    clientes.append(cliente)


def deletar(cliente):
    clientes.remove(cliente)


# Dicionário com as siglas e nomes das criptos
def listar():
    """
    :return: {...'BTC': 'Bitcoin', 'NANO': 'Nano'...}
    """
    dict_criptos_completo = cryptocompare.get_coin_list(format=False)
    dict_criptos = {}
    for sigla, nome in dict_criptos_completo.items():
        dict_criptos[sigla] = nome['CoinName']
    return dict_criptos


clientes = [Cliente(1, "Ruann Yury", 100, '200.100.345-34', 'fisica'),
            Cliente(2, "Israelzin", 200, '200.100.346-34', 'fisica'),
            Cliente(3, "Rafolas", 300, '200.100.347-34', 'juridica')]


@app.route("/home")
@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/currency", methods=['GET', 'POST'])
def currency():
    if request.method == 'POST':
        nome = request.form['moeda']
        sigla = request.form['sigla']
        preco = cryptocompare.get_price(sigla.upper(), currency=nome.upper())
        _str = f'Um {sigla.upper()} está valendo {preco[sigla.upper()][nome.upper()]} {nome.upper()}!'
        flash(_str)
        return redirect(url_for('currency'))
    return render_template('currency.html')


@app.route("/portfolio", methods=['GET', 'POST'])
def portfolio():
    if request.method == 'POST':
        cliente_id = int(request.form['id'])
        cliente = [c for c in clientes if cliente_id == c.get_id()][0]
        cliente.set_nome(request.form['nome'])
        cliente.set_cnpjcpf(request.form['cpfcnpj'])
        flash('Atualizado!')
        return redirect(url_for('visualizar'))
    return render_template('portfolio.html')


@app.route("/visualizar")
def visualizar():
    siglas_nomes = listar()
    return render_template('visualizar.html', siglas_nomes=siglas_nomes)
