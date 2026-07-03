from datetime import datetime
from flask import Blueprint, redirect, render_template, request, url_for
from models import ClienteLocadora, Locacao, Veiculo, db

locadora_bp = Blueprint("locadora", __name__, url_prefix="/locadora")


@locadora_bp.route("/")
def index():
    locacoes = Locacao.listar_com_detalhes()
    return render_template("locadora/lista.html", locacoes=locacoes)


# -----------------------------------------------------------------------------
# NOVA ROTA: CADASTRO DE CLIENTES
# -----------------------------------------------------------------------------
@locadora_bp.route("/cadastrar_cliente", methods=["GET", "POST"])
def cadastrar_cliente():
    if request.method == "POST":
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        cnh = request.form.get("cnh")

        novo_cliente = ClienteLocadora(nome=nome, cpf=cpf, cnh=cnh)
        db.session.add(novo_cliente)
        db.session.commit()
        
        # Depois de salvar, volta para o formulário de locação
        return redirect(url_for("locadora.cadastrar"))

    return render_template("locadora/cadastrar_cliente.html")


# -----------------------------------------------------------------------------
# NOVA ROTA: CADASTRO DE VEÍCULOS
# -----------------------------------------------------------------------------
@locadora_bp.route("/cadastrar_veiculo", methods=["GET", "POST"])
def cadastrar_veiculo():
    if request.method == "POST":
        modelo = request.form.get("modelo")
        placa = request.form.get("placa")
        diaria = float(request.form.get("diaria"))

        novo_veiculo = Veiculo(modelo=modelo, placa=placa, diaria=diaria)
        db.session.add(novo_veiculo)
        db.session.commit()
        
        # Depois de salvar, volta para o formulário de locação
        return redirect(url_for("locadora.cadastrar"))

    return render_template("locadora/cadastrar_veiculo.html")


# ROTA DE LOCAÇÃO (JÁ EXISTENTE)
@locadora_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    clientes = ClienteLocadora.listar()
    veiculos = Veiculo.listar()

    if request.method == "POST":
        cliente_id = request.form.get("cliente_id")
        veiculo_id = request.form.get("veiculo_id")
        
        data_ini_str = request.form.get("data_inicio")
        data_fim_str = request.form.get("data_fim")
        data_inicio = datetime.strptime(data_ini_str, "%Y-%m-%d").date()
        data_fim = datetime.strptime(data_fim_str, "%Y-%m-%d").date()
        
        valor_total = float(request.form.get("valor_total"))

        nova_locacao = Locacao(
            cliente_id=cliente_id,
            veiculo_id=veiculo_id,
            data_inicio=data_inicio,
            data_fim=data_fim,
            valor_total=valor_total
        )

        db.session.add(nova_locacao)
        db.session.commit()
        return redirect(url_for("locadora.index"))

    return render_template(
        "locadora/formulario.html",
        clientes=clientes,
        veiculos=veiculos,
    )