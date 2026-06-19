from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .base import ModeloBase
from .cliente_locadora import ClienteLocadora
from .veiculo import Veiculo
from .locacao import Locacao

__all__ = ["db", "ModeloBase", "ClienteLocadora", "Veiculo", "Locacao"]