# Model seguro: senha em hash, cadastro sempre como visitante, senha nunca no JSON.

from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .base import ModeloBase

PAPEIS = ("admin", "piloto", "visitante")


class Usuario(ModeloBase):
    """Usuario da torre."""

    __tablename__ = "usuarios"

    username = db.Column(db.String(40), nullable=False, unique=True)
    nome = db.Column(db.String(120), nullable=False)
    # Nunca texto puro: sempre um hash (werkzeug generate_password_hash).
    senha_hash = db.Column(db.String(255), nullable=False)
    papel = db.Column(db.String(20), nullable=False, default="visitante")

    def definir_senha(self, senha: str) -> None:
        self.senha_hash = generate_password_hash(senha)

    def senha_confere(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha or "")

    @classmethod
    def buscar_por_username(cls, username: str):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.username).all()

    @classmethod
    def a_partir_de_dict(cls, dados: dict):
        try:
            username = str(dados["username"]).strip().lower()
            nome = str(dados.get("nome") or username).strip()
            senha = str(dados["senha"])
            # Cadastro público sempre entra como visitante — cliente não escolhe o papel.
            papel = "visitante"
        except (KeyError, TypeError) as erro:
            raise ValueError("Campos obrigatórios: username e senha") from erro

        if cls.buscar_por_username(username):
            raise ValueError("username já cadastrado")

        usuario = cls(username=username, nome=nome, papel=papel)
        usuario.definir_senha(senha)
        return usuario

    def para_dict(self) -> dict:
        # Nunca devolve senha nem hash no JSON.
        return {
            "id": self.id,
            "username": self.username,
            "nome": self.nome,
            "papel": self.papel,
            "data_criacao": str(self.data_criacao),
        }
