from . import db
from .base import ModeloBase


class Locacao(ModeloBase):
    __tablename__ = "locacoes"

    # Chaves Estrangeiras (FK) ligando aos IDs das outras tabelas
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes_locadora.id"), nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey("veiculos.id"), nullable=False)
    
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)

    # Relacionamentos para acessar os dados dos objetos vinculados
    cliente = db.relationship("ClienteLocadora", back_populates="locacoes")
    veiculo = db.relationship("Veiculo", back_populates="locacoes")

    @classmethod
    def listar_com_detalhes(cls):
        return cls.query.order_by(cls.data_criacao.desc()).all()