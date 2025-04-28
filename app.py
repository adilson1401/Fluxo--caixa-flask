from flask import Flask, render_template_string, request, redirect, url_for, session
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'chave_secreta'

# Usuário fixo
USUARIO = 'adilson'
SENHA = 'adrcosta'

# Arquivo para salvar vendas
ARQUIVO_VENDAS = 'vendas.json'

# Carregar vendas do arquivo
def carregar_vendas():
    if os.path.exists(ARQUIVO_VENDAS):
        with open(ARQUIVO_VENDAS, 'r') as f:
            return json.load(f)
    return []

# Salvar vendas no arquivo
def salvar_vendas(vendas):
    with open(ARQUIVO_VENDAS, 'w') as f:
        json.dump(vendas, f, indent=4)

# Lista de vendas
vendas = carregar_vendas()

# HTML templates com estilo
template_login = """
<!DOCTYPE html>
<html>
<head>
<title>Login</title>
<style>
body { font-family: Arial; background-color: #f2f2f2; padding: 20px; }
form { background: white; padding: 20px; border-radius: 10px; width: 300px; margin: auto; }
input[type=text], input[type=password] { width: 100%; padding: 10px; margin: 5px 0; }
input[type=submit] { background-color: #4CAF50; color: white; padding: 10px; border: none; width: 100%; border-radius: 5px; }
p { text-align: center; }
</style>
</head>
<body>
<h2 style="text-align:center;">Login</h2>
<form method="post">
  <input type="text" name="usuario" placeholder="Usuário" required>
  <input type="password" name="senha" placeholder="Senha" required><br><br>
  <input type="submit" value="Entrar">
</form>
{% if erro %}
<p style="color:red;">{{ erro }}</p>
{% endif %}
</body>
</html>
"""

template_fluxo = """
<!DOCTYPE html>
<html>
<head>
<title>Fluxo de Caixa</title>
<style>
body { font-family: Arial; background-color: #e6e6e6; padding: 20px; }
form { background: white; padding: 20px; border-radius: 10px; width: 400px; margin-bottom: 30px; }
input[type=text], input[type=number], select { width: 100%; padding: 10px; margin: 5px 0; }
input[type=submit] { background-color: #007BFF; color: white; padding: 10px; border: none; width: 100%; border-radius: 5px; }
table { width: 100%; border-collapse: collapse; margin-top: 20px; }
table, th, td { border: 1px solid black; }
th, td { padding: 10px; text-align: center; }
h2, h3 { text-align: center; }
a { display: block; text-align: center; margin-top: 20px; color: #007BFF; text-decoration: none; }
</style>
</head>
<body>

<h2>Fluxo de Caixa</h2>
<form method="post">
  Nome do Cliente: <input type="text" name="cliente" required><br>
  Procedimento: <input type="text" name="procedimento" required><br>
  Forma de Pagamento:
  <select name="forma_pagamento" required>
    <option>Dinheiro</option>
    <option>Pix</option>
    <option>Débito</option>
    <option>Crédito</option>
    <option>Pix Itaú</option>
  </select><br>
  Valor: <input type="number" step="0.01" name="valor" required><br><br>
  <input type="submit" value="Registrar Venda">
</form>

<h3>Vendas Registradas</h3>
<table>
<tr>
<th>Data</th><th>Cliente</th><th>Procedimento</th><th>Forma Pagamento</th><th>Valor (R$)</th>
</tr>
{% for venda in vendas %}
<tr>
<td>{{ venda['data'] }}</td>
<td>{{ venda['cliente'] }}</td>
<td>{{ venda['procedimento'] }}</td>
<td>{{ venda['forma_pagamento'] }}</td>
<td>{{ venda['valor'] }}</td>
</tr>
{% endfor %}
</table>

<h3>Totais</h3>
<ul>
<li>Dinheiro: R$ {{ totais['Dinheiro'] }}</li>
<li>Pix: R$ {{ totais['Pix'] }}</li>
<li>Débito: R$ {{ totais['Débito'] }}</li>
<li>Crédito: R$ {{ totais['Crédito'] }}</li>
<li>Pix Itaú: R$ {{ totais['Pix Itaú'] }}</li>
</ul>

<a href="{{ url_for('logout') }}">Sair</a>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario == USUARIO and senha == SENHA:
            session['logado'] = True
            return redirect(url_for('fluxo'))
        else:
            erro = "Usuário ou senha incorretos."
    return render_template_string(template_login, erro=erro)

@app.route('/fluxo', methods=['GET', 'POST'])
def fluxo():
    if not session.get('logado'):
