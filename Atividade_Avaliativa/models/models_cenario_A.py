"""
ATIVIDADE AULA 11 — Models por cenário (1,0 ponto)

Aluno: Thaís De Michelis
Cenário escolhido (A, B ou C): A
  A = Locadora de veículos
  B = Cinema
  C = Troca de figurinhas Copa do Mundo

Renomeie este arquivo para: models_cenario_A.py
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ModeloBase(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )
    data_atualizacao = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


# =============================================================================
# TABELAS DO CENÁRIO A — LOCADORA DE VEÍCULOS
# =============================================================================


class ClienteLocadora(ModeloBase):
    __tablename__ = "clientes_locadora"

    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    cnh = db.Column(db.String(15), nullable=False, unique=True)

    # Relacionamento para acessar as locações do cliente
    locacoes = db.relationship("Locacao", back_populates="cliente")

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.nome).all()


class Veiculo(ModeloBase):
    __tablename__ = "veiculos"

    placa = db.Column(db.String(10), nullable=False)
    modelo = db.Column(db.String(80), nullable=False)
    diaria = db.Column(db.Float, nullable=False)

    # Relacionamento para acessar as locações do veículo
    locacoes = db.relationship("Locacao", back_populates="veiculo")

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.modelo).all()


class Locacao(ModeloBase):
    __tablename__ = "locacoes"

    # Chaves Estrangeiras ligando às tabelas de clientes e veículos
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes_locadora.id"), nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey("veiculos.id"), nullable=False)
    
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)

    # Relacionamentos inversos para permitir navegação pelo objeto
    cliente = db.relationship("ClienteLocadora", back_populates="locacoes")
    veiculo = db.relationship("Veiculo", back_populates="locacoes")

    @classmethod
    def listar_com_detalhes(cls):
        return cls.query.order_by(cls.data_criacao.desc()).all()