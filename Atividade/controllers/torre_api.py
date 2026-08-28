# Radar e admin protegidos: JWT obrigatório + checagem de papel para admin.

from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify
from flask_jwt_extended import current_user, get_jwt, jwt_required

from models import TokenRevogado, Usuario
from services import listar_voos_radar

torre_api_bp = Blueprint("torre_api", __name__, url_prefix="/api/torre")


def _exige_admin():
    if get_jwt().get("papel") != "admin":
        return jsonify({"erro": "Acesso restrito a administradores."}), 403
    return None


@torre_api_bp.route("/saguao", methods=["GET"])
@jwt_required(optional=True)
def saguao() -> Any:
    if current_user:
        return jsonify({"lugar": "saguão", "logado": True, "mensagem": f"Olá, {current_user.nome}."})
    return jsonify({"lugar": "saguão", "logado": False, "mensagem": "Anônimo no saguão."})


@torre_api_bp.route("/radar", methods=["GET"])
@jwt_required()
def radar() -> Any:
    return jsonify(
        {
            "mensagem": "Radar (protegido por JWT)",
            **listar_voos_radar(),
        }
    )


@torre_api_bp.route("/admin", methods=["GET"])
@jwt_required()
def admin() -> Any:
    recusa = _exige_admin()
    if recusa:
        return recusa
    usuarios = [u.para_dict() for u in Usuario.listar()]
    return jsonify(
        {
            "mensagem": "Sala de controle — acesso restrito a admin",
            "usuarios": usuarios,
            "total_usuarios": len(usuarios),
        }
    )


@torre_api_bp.route("/blocklist", methods=["GET"])
@jwt_required()
def blocklist() -> Any:
    recusa = _exige_admin()
    if recusa:
        return recusa
    tokens = TokenRevogado.listar()
    return jsonify({"banco": "blocklist.db", "total": len(tokens), "tokens": [t.para_dict() for t in tokens]})
