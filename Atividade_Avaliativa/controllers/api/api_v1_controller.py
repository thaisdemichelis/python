from datetime import datetime

from flask import Blueprint, jsonify, request

from models import ClienteLocadora, Locacao, Veiculo, db
from services import modelos_por_marca

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")


@api_v1_bp.route("/locacoes", methods=["GET"])
def api_listar_locacoes():
    locacoes = Locacao.listar_com_detalhes()
    return jsonify([
        {
            "id": loc.id,
            "cliente": loc.cliente.nome,
            "veiculo": loc.veiculo.modelo,
            "placa": loc.veiculo.placa,
            "data_inicio": loc.data_inicio.isoformat(),
            "data_fim": loc.data_fim.isoformat(),
            "valor_total": loc.valor_total,
        }
        for loc in locacoes
    ])


@api_v1_bp.route("/locacoes/<int:locacao_id>", methods=["GET"])
def api_detalhe_locacao(locacao_id):
    loc = db.session.get(Locacao, locacao_id)
    if not loc:
        return jsonify({"erro": "Locação não encontrada"}), 404
    return jsonify({
        "id": loc.id,
        "cliente": loc.cliente.nome,
        "veiculo": loc.veiculo.modelo,
        "placa": loc.veiculo.placa,
        "valor_total": loc.valor_total,
    })


@api_v1_bp.route("/locacoes", methods=["POST"])
def api_criar_locacao():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Envie JSON no body"}), 400
    try:
        loc = Locacao(
            cliente_id=int(dados["cliente_id"]),
            veiculo_id=int(dados["veiculo_id"]),
            data_inicio=datetime.strptime(dados["data_inicio"], "%Y-%m-%d").date(),
            data_fim=datetime.strptime(dados["data_fim"], "%Y-%m-%d").date(),
            valor_total=float(dados["valor_total"]),
        )
    except (KeyError, ValueError):
        return jsonify({"erro": "Campos inválidos"}), 400
    db.session.add(loc)
    db.session.commit()
    return jsonify({"id": loc.id, "mensagem": "Locação criada"}), 201


@api_v1_bp.route("/veiculos", methods=["GET"])
def api_listar_veiculos():
    return jsonify([
        {"id": v.id, "placa": v.placa, "modelo": v.modelo, "diaria": v.diaria}
        for v in Veiculo.listar()
    ])


@api_v1_bp.route("/veiculos/<int:veiculo_id>", methods=["GET"])
def api_detalhe_veiculo(veiculo_id):
    veiculo = db.session.get(Veiculo, veiculo_id)
    if not veiculo:
        return jsonify({"erro": "Veículo não encontrado"}), 404
    return jsonify({
        "id": veiculo.id,
        "placa": veiculo.placa,
        "modelo": veiculo.modelo,
        "diaria": veiculo.diaria,
    })


@api_v1_bp.route("/clientes", methods=["GET"])
def api_listar_clientes():
    return jsonify([
        {"id": c.id, "nome": c.nome, "cpf": c.cpf}
        for c in ClienteLocadora.listar()
    ])


@api_v1_bp.route("/externo/modelos", methods=["GET"])
def api_modelos_nhtsa():
    marca = request.args.get("marca", "Honda")
    try:
        modelos = modelos_por_marca(marca)[:25]
        return jsonify({"marca": marca, "fonte": "NHTSA vPIC", "modelos": modelos})
    except Exception:
        return jsonify({"erro": "Falha ao consultar API NHTSA"}), 502


@api_v1_bp.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "API está funcionando"}), 200
