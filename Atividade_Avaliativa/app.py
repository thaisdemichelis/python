import os
from flask import Flask, redirect
from models import db, ClienteLocadora, Veiculo


def criar_app():
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="views/static",
    )

    pasta = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        pasta, "pedidos.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializa o banco de dados único do projeto
    db.init_app(app)
    
    # Importa e registra as rotas da locadora
    from controllers import locadora_bp
    app.register_blueprint(locadora_bp)

    # Redireciona a página inicial direto para o sistema da locadora
    @app.route("/")
    def raiz():
        return redirect("/locadora/")

    with app.app_context():
        # Cria fisicamente as tabelas dentro do arquivo pedidos.db
        db.create_all()

        # SE O BANCO ESTIVER VAZIO, CRIA DADOS DE TESTE AUTOMATICAMENTE
        if ClienteLocadora.query.count() == 0:
            c1 = ClienteLocadora(nome="Ana Silva", cpf="111.111.111-11", cnh="12345678901")
            c2 = ClienteLocadora(nome="Carlos Souza", cpf="222.222.222-22", cnh="98765432109")
            
            v1 = Veiculo(modelo="Fiat Uno 1.0", placa="ABC-1234", diaria=80.0)
            v2 = Veiculo(modelo="Toyota Corolla", placa="XYZ-9876", diaria=250.0)
            
            db.session.add_all([c1, c2, v1, v2])
            db.session.commit()

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)