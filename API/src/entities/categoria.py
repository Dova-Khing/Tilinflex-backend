"""
ENTIDAD CATEGORIA
Define los tipos de medios audiovisuales del sistema.
"""

import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel, Field

from .base import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id_categoria = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    nombre_categoria = Column(
        String(50),
        nullable=False,
        unique=True
    )

    # Una categoría tiene muchas obras
    obras = relationship(
        "Obra",
        back_populates="categoria"
    )

    def __repr__(self):
        return f"<Categoria(nombre_categoria='{self.nombre_categoria}')>"
