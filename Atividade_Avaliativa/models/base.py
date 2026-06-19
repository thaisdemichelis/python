"""
Copie esta superclasse para sua entrega da atividade.
"""

from datetime import datetime
from . import db


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