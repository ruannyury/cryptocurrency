<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <link
      rel="stylesheet"
      href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
      integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh"
      crossorigin="anonymous"
    />
    <link
      rel="stylesheet"
      href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
      crossorigin="anonymous"
    />

    <title>{% block title %}Home{% endblock %}</title>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbar">
            <div class="navbar-nav">
                <a class="nav-item nav-link"><b>Portfolio Crypto</b></a>
                {% if user.is_authenticated %}
                <a class="nav-item nav-link" id="home" href="/">Home</a>
                <a class="nav-item nav-link" id="logout" href="/logout">Logout</a>
                <a class="nav-item nav-link" id="edit" href="/editportfolio">Editar portfolio</a>
                {% else %}
                <a class="nav-item nav-link" id="login" href="/index_login">Login</a>
                <a class="nav-item nav-link" id="signUp" href="/index_register">Sign Up</a>
                {% endif %}
            </div>
        </div>
    </nav>

    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                {% if category == 'error' %}
                    <div class="alert alert-danger alter-dismissable fade show" role="alert">
                        {{ message }}
                        <button type="button" class="close" data-dismiss="alert">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                {% else %}
                    <div class="alert alert-success alter-dismissable fade show" role="alert">
                        {{ message }}
                        <button type="button" class="close" data-dismiss="alert">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                {% endif %}
            {% endfor %}
        {% endif %}
    {% endwith %}

    <div class="container">
        {% block content %}
        {% endblock %}
    </div>


    <script
      src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
      integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
      crossorigin="anonymous"
    ></script>
    <script
      src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
      integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
      crossorigin="anonymous"
    ></script>
    <script
      src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
      integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
      crossorigin="anonymous"
    ></script>

    <script
      type="text/javascript"
      src="{{ url_for('static', filename='index.js') }}"
    ></script>


    <!--
    No campo src da tag img abaixo enviaremos 4 parametros via GET
    l = largura da imagem
    a = altura da imagem
    tf = tamanho fonte das letras
    ql = quantidade de letras do captcha
    -->
    <img src="captcha.php?l=150&a=50&tf=20&ql=5">
    <!--
    O texto digitado no campo abaixo sera enviado via POST para
    o arquivo validar.php que ira vereficar se o que voce digitou é igual
    ao que foi gravado na sessao pelo captcha.php
    -->
    <form action="validar_login.php" name="form" method="post">
        <input type="text" name="palavra"  />
        <input type="submit" value="Validar Captcha" />
    </form>
    

</body>
</html>