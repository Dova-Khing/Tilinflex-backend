"""
ENTIDAD GENERO
MODELO DE DATOS PARA LA ENTIDAD GENERO
"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Genero(Base):
    """
    Modelo de Genero que representa la tabla 'generos'

    Atributos:
        id_genero: Identificador único
        nombre_genero: Nombre del género
        fecha_registro: Fecha de creación
        fecha_actualizacion: Fecha de actualización
    """

    __tablename__ = 'generos'

    id_genero: uuid.UUID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    nombre_genero: str = Column(
        String(100),
        nullable=False,
        unique=True
    )

    fecha_registro: datetime = Column(
        DateTime,
        default=datetime.utcnow
    )

    fecha_actualizacion: datetime = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # --------------------
    # RELACION
    # --------------------

    obras = relationship(
        "Obra",
        back_populates="genero",
        cascade="all, delete"
    )

    def __repr__(self) -> str:
        return (
            f"<Genero(id_genero={self.id_genero}, "
            f"nombre_genero='{self.nombre_genero}')>"
        )

    def __to_dict__(self) -> dict:
        return {
            "id_genero": str(self.id_genero),
            "nombre_genero": self.nombre_genero,
            "fecha_registro": self.fecha_registro.isoformat(),
            "fecha_actualizacion": self.fecha_actualizacion.isoformat()
        }
"""
ESQUEMAS DE PYDANTIC PARA GENERO
"""

class GeneroBase(BaseModel):

    nombre_genero: str = Field(
        ...,
        example="Acción",
        min_length=3,
        max_length=100
    )

    @validator('nombre_genero')
    def validar_nombre_genero(cls, v):
        if not v.strip():
            raise ValueError("El nombre del género no puede estar vacío")
            return v.title()
class GeneroCreate(GeneroBase):
    pass
class GeneroUpdate(BaseModel):
    nombre_genero: Optional[str]

class GeneroResponse(GeneroBase):
    id_genero: uuid.UUID
    fecha_registro: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True
