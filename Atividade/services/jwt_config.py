# Callbacks JWT: claims de papel/nome e checagem de blocklist implementados.

from flask import jsonify
from flask_jwt_extended import JWTManager

from models import TokenRevogado, Usuario

jwt = JWTManager()


def configurar_jwt(app):
    jwt.init_app(app)
    return jwt


@jwt.user_identity_loader
def identidade_do_usuario(usuario):
    if hasattr(usuario, "id"):
        return str(usuario.id)
    return str(usuario)


@jwt.user_lookup_loader
def carregar_usuario(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Usuario.query.filter_by(id=int(identity)).one_or_none()


@jwt.additional_claims_loader
def claims_extras(identity):
    # identity aqui é o objeto original passado a create_access_token (antes do
    # user_identity_loader transformar em id), então já temos papel/nome direto.
    usuario = identity if hasattr(identity, "papel") else Usuario.query.filter_by(id=identity).one_or_none()
    if usuario is None:
        return {}
    return {"papel": usuario.papel, "nome": usuario.nome}


@jwt.token_in_blocklist_loader
def token_esta_na_blocklist(_jwt_header, jwt_payload: dict) -> bool:
    return TokenRevogado.esta_revogado(jwt_payload.get("jti"))


@jwt.expired_token_loader
def token_expirado(_jwt_header, jwt_payload):
    return jsonify({"erro": "Token expirado", "tipo": jwt_payload.get("type")}), 401


@jwt.invalid_token_loader
def token_invalido(motivo: str):
    return jsonify({"erro": "Token inválido", "detalhe": motivo}), 401


@jwt.unauthorized_loader
def token_ausente(motivo: str):
    return jsonify({"erro": "Token ausente", "detalhe": motivo}), 401


@jwt.revoked_token_loader
def token_revogado(_jwt_header, _jwt_payload):
    return jsonify({"erro": "Token revogado (logout). Faça login de novo."}), 401


@jwt.needs_fresh_token_loader
def precisa_token_fresh(_jwt_header, _jwt_payload):
    return jsonify({"erro": "Esta operação exige um token fresh"}), 401


@jwt.user_lookup_error_loader
def usuario_sumiu(_jwt_header, _jwt_payload):
    return jsonify({"erro": "Usuário do token não existe mais"}), 401
