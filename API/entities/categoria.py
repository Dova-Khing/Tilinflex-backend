"""
ENTIDAD CATEGORIA
MODELO DE DATOS PARA LA ENTIDAD CATEGORIA
"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Categoria(Base):
    """
    Modelo de Categoria que representa la tabla 'categorias'

    Atributos:
        id_categoria: Identificador único
        nombre_categoria: Nombre de la categoría
        fecha_registro: Fecha de creación
        fecha_actualizacion: Fecha de actualización
    """

    __tablename__ = 'categorias'

    id_categoria: uuid.UUID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    nombre_categoria: str = Column(String(100), nullable=False, unique=True)

    fecha_registro: datetime = Column(
        DateTime,
        default=datetime.utcnow
    )

    fecha_actualizacion: datetime = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # RELACION: Una categoria tiene muchas obras
    obras = relationship(
        "Obra",
        back_populates="categoria",
        cascade="all, delete"
    )

    def __repr__(self) -> str:
        return (
            f"<Categoria(id_categoria={self.id_categoria}, "
            f"nombre_categoria='{self.nombre_categoria}')>"
        )

    def __to_dict__(self) -> dict:
        return {
            "id_categoria": str(self.id_categoria),
            "nombre_categoria": self.nombre_categoria,
            "fecha_registro": self.fecha_registro.isoformat(),
            "fecha_actualizacion": self.fecha_actualizacion.isoformat()
        }

"""
ESQUEMAS DE PYDANTIC PARA LA ENTIDAD CATEGORIA
"""

class CategoriaBase(BaseModel):
    """
    Esquema base para la entidad Categoria
    """

    nombre_categoria: str = Field(
        ...,
        example="Acción",
        min_length=3,
        max_length=100
    )

    @validator('nombre_categoria')
    def validate_nombre_categoria(cls, v):
        if not v.strip():
            raise ValueError("El nombre de la categoría no puede estar vacío")
        return v.title()
    
class CategoriaCreate(CategoriaBase):
    """
    Esquema para crear una nueva categoría
    """
    pass
