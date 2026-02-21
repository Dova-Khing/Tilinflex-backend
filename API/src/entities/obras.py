"""
ENTIDAD OBRA
MODELO DE DATOS PARA LA ENTIDAD OBRA
"""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Obra(Base):
    """
    Modelo de Obra que representa la tabla 'obras'

    Atributos:
        id_obra: Identificador único
        nombre: Nombre de la obra
        descripcion: Descripción de la obra
        episodios: Número de episodios
        anio: Año de lanzamiento
        id_categoria: FK hacia categoria
        id_genero: FK hacia genero
    """

    __tablename__ = 'obras'

    id_obra: uuid.UUID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    nombre: str = Column(String(150), nullable=False)

    descripcion: str = Column(Text, nullable=True)

    episodios: int = Column(Integer, nullable=False, default=1)

    anio: int = Column(Integer, nullable=False)

    fecha_registro: datetime = Column(
        DateTime,
        default=datetime.utcnow
    )

    # --------------------
    # FOREIGN KEYS
    # --------------------

    id_categoria: uuid.UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("categorias.id_categoria"),
        nullable=False
    )

    id_genero: uuid.UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("generos.id_genero"),
        nullable=False
    )

    # --------------------
    # RELACIONES
    # --------------------

    categoria = relationship(
        "Categoria",
        back_populates="obras"
    )

    generos = relationship(
        "Genero",
        back_populates="obras"
    )

    historial = relationship(
        "HistorialReproduccion",
        back_populates="obra",
        cascade="all, delete"
    )

    def __repr__(self) -> str:
        return (
            f"<Obra(id_obra={self.id_obra}, "
            f"nombre='{self.nombre}', anio={self.anio})>"
        )

    def __to_dict__(self) -> dict:
        return {
            "id_obra": str(self.id_obra),
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "episodios": self.episodios,
            "anio": self.anio,
            "fecha_registro": self.fecha_registro.isoformat(),
            "id_categoria": str(self.id_categoria),
            "id_genero": str(self.id_genero)
        }

"""
ESQUEMAS DE PYDANTIC PARA LA ENTIDAD OBRA
"""

class ObraBase(BaseModel):

    nombre: str = Field(..., example="Breaking Bad", min_length=2)
    descripcion: Optional[str] = Field(None, example="Serie sobre química...")
    episodios: int = Field(..., example=10, ge=1)
    anio: int = Field(..., example=2023, ge=1900)

    id_categoria: uuid.UUID
    id_genero: uuid.UUID

    @validator('anio')
    def validar_anio(cls, v):
        if v > datetime.utcnow().year:
            raise ValueError("El año no puede ser mayor al actual")
        return v
class ObraCreate(ObraBase):
    pass

class ObraUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    episodios: Optional[int]
    anio: Optional[int]

class ObraResponse(ObraBase):
    id_obra: uuid.UUID
    fecha_registro: datetime

    class Config:
        orm_mode = True
