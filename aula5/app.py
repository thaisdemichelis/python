from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'cotemig2026'

usuarios = {
    "marcos": "cotemig2026",
    "janaina": "cotemig2026",
    "12402036": "cotemig2026"
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario in usuarios and usuarios[usuario] == senha:
            session['usuario'] = usuario
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha inválidos')

    return render_template('index.html')

@app.route('/home')
def home():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', logged_in=True, usuario=session['usuario'])

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
   app.run(debug=True)