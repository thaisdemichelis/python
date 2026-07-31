from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import requests
import os

app = Flask(__name__)
app.secret_key = 'chave_secreta_flask_tarefas_2024'
app.config['DEBUG'] = False

DATABASE = 'tarefas.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT NOT NULL DEFAULT 'Pendente',
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')
    conn.commit()
    conn.close()

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        if not nome or not email or not senha:
            flash('Preencha todos os campos.', 'danger')
            return render_template('registro.html')
        senha_hash = generate_password_hash(senha)
        conn = get_db()
        try:
            conn.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)',
                         (nome, email, senha_hash))
            conn.commit()
            flash('Cadastro realizado com sucesso. Faça login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('E-mail já cadastrado.', 'danger')
        finally:
            conn.close()
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        conn = get_db()
        usuario = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
        conn.close()
        if usuario and check_password_hash(usuario['senha'], senha):
            session['usuario_id'] = usuario['id']
            session['usuario_nome'] = usuario['nome']
            return redirect(url_for('dashboard'))
        flash('E-mail ou senha inválidos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    status_filtro = request.args.get('status', '')
    conn = get_db()
    if status_filtro:
        tarefas = conn.execute(
            'SELECT * FROM tarefas WHERE usuario_id = ? AND status = ? ORDER BY id DESC',
            (session['usuario_id'], status_filtro)
        ).fetchall()
    else:
        tarefas = conn.execute(
            'SELECT * FROM tarefas WHERE usuario_id = ? ORDER BY id DESC',
            (session['usuario_id'],)
        ).fetchall()
    conn.close()
    frase = ''
    try:
        r = requests.get('https://api.adviceslip.com/advice', timeout=5)
        if r.status_code == 200:
            frase = r.json()['slip']['advice']
    except:
        frase = 'Continue focado nas suas metas.'
    return render_template('dashboard.html', tarefas=tarefas, frase=frase, status_filtro=status_filtro)

@app.route('/api/tarefas')
@login_required
def api_tarefas():
    status_filtro = request.args.get('status', '')
    conn = get_db()
    if status_filtro:
        tarefas = conn.execute(
            'SELECT id, titulo, descricao, status FROM tarefas WHERE usuario_id = ? AND status = ? ORDER BY id DESC',
            (session['usuario_id'], status_filtro)
        ).fetchall()
    else:
        tarefas = conn.execute(
            'SELECT id, titulo, descricao, status FROM tarefas WHERE usuario_id = ? ORDER BY id DESC',
            (session['usuario_id'],)
        ).fetchall()
    conn.close()
    return jsonify([dict(t) for t in tarefas])

@app.route('/nova_tarefa', methods=['GET', 'POST'])
@login_required
def nova_tarefa():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        descricao = request.form.get('descricao', '').strip()
        status = request.form.get('status', 'Pendente')
        if not titulo:
            flash('Título é obrigatório.', 'danger')
            return render_template('nova_tarefa.html')
        conn = get_db()
        conn.execute(
            'INSERT INTO tarefas (titulo, descricao, status, usuario_id) VALUES (?, ?, ?, ?)',
            (titulo, descricao, status, session['usuario_id'])
        )
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('nova_tarefa.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    conn = get_db()
    tarefa = conn.execute(
        'SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?',
        (id, session['usuario_id'])
    ).fetchone()
    if not tarefa:
        conn.close()
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        descricao = request.form.get('descricao', '').strip()
        status = request.form.get('status', 'Pendente')
        if not titulo:
            flash('Título é obrigatório.', 'danger')
            conn.close()
            return render_template('editar.html', tarefa=tarefa)
        conn.execute(
            'UPDATE tarefas SET titulo = ?, descricao = ?, status = ? WHERE id = ? AND usuario_id = ?',
            (titulo, descricao, status, id, session['usuario_id'])
        )
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    conn.close()
    return render_template('editar.html', tarefa=tarefa)

@app.route('/excluir/<int:id>')
@login_required
def excluir(id):
    conn = get_db()
    conn.execute(
        'DELETE FROM tarefas WHERE id = ? AND usuario_id = ?',
        (id, session['usuario_id'])
    )
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/concluir/<int:id>')
@login_required
def concluir(id):
    conn = get_db()
    conn.execute(
        'UPDATE tarefas SET status = ? WHERE id = ? AND usuario_id = ?',
        ('Concluída', id, session['usuario_id'])
    )
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/progresso')
@login_required
def progresso():
    return render_template('progresso.html')

@app.route('/api/progresso')
@login_required
def api_progresso():
    conn = get_db()
    dados = conn.execute(
        '''SELECT status, COUNT(*) as total
           FROM tarefas
           WHERE usuario_id = ?
           GROUP BY status''',
        (session['usuario_id'],)
    ).fetchall()
    conn.close()
    resultado = {'Pendente': 0, 'Em andamento': 0, 'Concluída': 0}
    for row in dados:
        if row['status'] in resultado:
            resultado[row['status']] = row['total']
    return jsonify(resultado)

@app.route('/api/tarefas_rest')
@login_required
def api_tarefas_rest():
    conn = get_db()
    tarefas = conn.execute(
        'SELECT id, titulo, descricao, status FROM tarefas WHERE usuario_id = ? ORDER BY id DESC',
        (session['usuario_id'],)
    ).fetchall()
    conn.close()
    return jsonify([dict(t) for t in tarefas])

if __name__ == '__main__':
    init_db()
    app.run(debug=False)