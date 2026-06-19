from . import db
from .base import ModeloBase


class ClienteLocadora(ModeloBase):
    __tablename__ = "clientes_locadora"

    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    cnh = db.Column(db.String(15), nullable=False, unique=True)

    # Faz o vínculo para conseguir puxar as locações a partir do cliente
    locacoes = db.relationship("Locacao", back_populates="cliente")

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.nome).all()