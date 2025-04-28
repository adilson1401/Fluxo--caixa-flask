from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_segura'  # Adicione uma chave secreta

# Função para carregar as vendas do arquivo JSON
def carregar_vendas():
    if not os.path.exists('vendas.json'):
        return []
    with open('vendas.json', 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# Função para salvar as vendas no arquivo JSON
def salvar_vendas(vendas):
    with open('vendas.json', 'w') as f:
        json.dump(vendas, f, indent=4)

@app.route('/')
def index():
    if not session.get('logado'):
        return redirect(url_for('login'))
    vendas = carregar_vendas()
    return render_template('index.html', vendas=vendas)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    if not session.get('logado'):
        return redirect(url_for('login'))
    produto = request.form['produto']
    quantidade = request.form['quantidade']
    preco = request.form['preco']

    vendas = carregar_vendas()
    vendas.append({
        'produto': produto,
        'quantidade': quantidade,
        'preco': preco
    })
    salvar_vendas(vendas)

    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        # Aqui está o login fixo para exemplo
        if usuario == 'admin' and senha == 'senha123':
            session['logado'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', erro='Usuário ou senha inválidos.')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)