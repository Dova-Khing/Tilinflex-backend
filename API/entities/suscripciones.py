"""
ENTIDAD SUSCRIPCIONES
MODELO DE DATOS PARA LA ENTIDAD SUSCRIPCIONES
"""



from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import os

from .base import Base


class Suscripcion(Base):
    """
    Modelo de Suscripcion que representa la tabla 'suscripciones'

    Atributos:
        id_suscripcion: Identificador único
        tipo_suscripcion: Tipo de suscripción (mensual, anual, etc.)
        fecha_inicio: Fecha de inicio de la suscripción
        fecha_fin: Fecha de fin de la suscripción
        id_detalle_suscripcion FK: Identificador de detalle de suscripción (si aplica)
    """

__tablename__ = 'suscripciones'
id_suscripcion: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
tipo_suscripcion: str = Column(String(50), nullable=False)
fecha_inicio: datetime = Column(DateTime, default=datetime.utcnow)
fecha_fin: datetime = Column(DateTime, nullable=True)
id_detalle_suscripcion: Optional[uuid.UUID] = Column(UUID(as_uuid=True), nullable=True)

usuarios = relationship(
    "Usuario", back_populates="suscripcion", uselist=True)

detalle_suscripcion = relationship("DetalleSuscripcion",
                                   back_populates="suscripcion")


def __repr__(self) -> str:
        return f"<Suscripcion(id de la suscripcion={self.id_suscripcion}, tipo de suscripcion='{self.tipo_suscripcion}', fecha de inicio='{self.fecha_inicio}', fecha de fin='{self.fecha_fin}')>"

def __to_dict__(self) -> dict:
        return {
            "id de la suscripcion": str(self.id_suscripcion),
            "tipo de suscripcion": self.tipo_suscripcion,
            "fecha de inicio": self.fecha_inicio.isoformat(),
            "fecha de fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
            "id detalle de la suscripcion": str(self.id_detalle_suscripcion) if self.id_detalle_suscripcion else None
        }

"""
ESQUEMAAS DE PYDANTIC PARA LA ENTIDAD SUSCRIPCIONES
"""

class SuscripcionBase(BaseModel):
    """
    Esquema base para la entidad Suscripcion
    """
    tipo_suscripcion: str = Field(..., example="mensual")
    fecha_inicio: Optional[datetime] = Field(default_factory=datetime.utcnow, example="2024-01-01T00:00:00Z")
    fecha_fin: Optional[datetime] = Field(None, example="2024-12-31T23:59:59Z")
    id_detalle_suscripcion: Optional[uuid.UUID] = Field(None, example=str(uuid.uuid4()))

    @validator('tipo_suscripcion')
    def validate_tipo_suscripcion(cls, v):
        if v not in ['mensual', 'anual', 'trimestral']:
            raise ValueError("El tipo de suscripción debe ser 'mensual', 'anual' o 'trimestral'")
        return v

    @validator('fecha_fin')
    def validate_fecha_fin(cls, v, values):
        if v and 'fecha_inicio' in values and v < values['fecha_inicio']:
            raise ValueError("La fecha de fin no puede ser anterior a la fecha de inicio")
        return v

class SuscripcionCreate(SuscripcionBase):
    """
    Esquema para crear una nueva suscripción
    """
    pass

class SuscripcionUpdate(BaseModel):
    tipo_suscripcion: Optional[str] = Field(None)

class SuscripcionResponse(SuscripcionBase):
    id_suscripcion: uuid.UUID = Field(..., example=str(uuid.uuid4()))

    class Config:
        orm_mode = True
