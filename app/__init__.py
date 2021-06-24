from flask import Flask, request, url_for, redirect, render_template, flash
from app.models.tables import Cliente


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


# Instanciar os Clientes
clientes = [Cliente(1, "Ruann Yury", 100, '200.100.345-34', 'fisica'),
            Cliente(2, "Israelzin", 200, '200.100.346-34', 'fisica'),
            Cliente(3, "Rafolas", 300, '200.100.347-34', 'juridica')]


@app.route("/home")
@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/adicionar", methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        cliente = Cliente(global_id, request.form['nome'], global_codigo, request.form['cpfcnpj'], 'fisica')
        atualizar_1(cliente)
        flash('Adicionado!')
        return redirect(url_for('visualizar'))
    return render_template('adicionar.html')


@app.route("/visualizar")
def visualizar():
    return render_template('visualizar.html', clientes=clientes)


@app.route("/atualizar", methods=['GET', 'POST'])
def atualizar():
    if request.method == 'POST':
        cliente_id = int(request.form['id'])
        cliente = [c for c in clientes if cliente_id == c.get_id()][0]
        cliente.set_nome(request.form['nome'])
        cliente.set_cnpjcpf(request.form['cpfcnpj'])
        flash('Atualizado!')
        return redirect(url_for('visualizar'))
    return render_template('atualizar.html')


@app.route("/remover", methods=['GET', 'POST'])
def remover():
    if request.method == 'POST':
        cliente_id = int(request.form['id'])
        cliente = [c for c in clientes if cliente_id == c.get_id()][0]
        deletar(cliente)
        return render_template('remover.html', cliente=cliente)
    else:
        return render_template('remover.html')
