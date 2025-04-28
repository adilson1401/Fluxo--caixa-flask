from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'chave_secreta_qualquer'

def carregar_vendas():
    try:
        with open('vendas.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_vendas(vendas):
    with open('vendas.json', 'w') as f:
        json.dump(vendas, f)

@app.route('/')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    vendas = carregar_vendas()
    return render_template('index.html', vendas=vendas)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    produto = request.form['produto']
    quantidade = request.form['quantidade']
    preco = request.form['preco']

    vendas = carregar_vendas()
    vendas.append({'produto': produto, 'quantidade': quantidade, 'preco': preco})
    salvar_vendas(vendas)
    
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        
        if usuario == 'adilson' and senha == 'adrcosta':
            session['usuario'] = usuario
            return redirect(url_for('index'))
        else:
            return render_template('login.html', erro='Usuário ou senha incorretos')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()