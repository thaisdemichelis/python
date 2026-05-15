from flask import Flask, render_template # render template é usado para buscar o arquivo html e mostrar para o usuário


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html') # chamei o que eu importei (agora falamos que isso é renderizar o arquivo)

@app.route('/sobre/<nome>') # aqui é um conteúdo dinâmico, ou seja, o nome pode ser qualquer coisa, e ele vai mostrar a mensagem personalizada
def sobre(nome):
    return  f'Olá, {nome}! Bem-vindo à página.'

if __name__ == '__main__':
    app.run(debug=True)
