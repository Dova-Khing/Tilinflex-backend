"""
ENTIDAD HISTORIAL_REPRODUCCION
MODELO DE DATOS PARA LA ENTIDAD HISTORIAL_REPRODUCCION
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class HistorialReproduccion(Base):
    """
    Modelo de HistorialReproduccion que representa la tabla 'historial_reproduccion'
    """

    __tablename__ = "historial_reproduccion"

    id_historial: uuid.UUID = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    tiempo_visto: int = Column(Integer, nullable=False)

    fecha_visualizacion: datetime = Column(DateTime, default=datetime.utcnow)

    # --------------------
    # FOREIGN KEYS
    # --------------------

    id_perfil: uuid.UUID = Column(
        UUID(as_uuid=True), ForeignKey("perfiles.id_perfil"), nullable=False
    )

    id_obra: uuid.UUID = Column(
        UUID(as_uuid=True), ForeignKey("obras.id_obra"), nullable=False
    )

    # --------------------
    # RELACIONES
    # --------------------

    perfil = relationship("Perfil", back_populates="historial_reproduccion")
    obra = relationship("Obra", back_populates="historial")

    def __repr__(self) -> str:
        return (
            f"<HistorialReproduccion(id_historial={self.id_historial}, "
            f"tiempo_visto={self.tiempo_visto})>"
        )

    def __to_dict__(self) -> dict:
        return {
            "id_historial": str(self.id_historial),
            "tiempo_visto": self.tiempo_visto,
            "fecha_visualizacion": self.fecha_visualizacion.isoformat(),
            "id_perfil": str(self.id_perfil),
            "id_obra": str(self.id_obra),
        }


"""
ESQUEMAS DE PYDANTIC PARA HISTORIAL_REPRODUCCION
"""


class HistorialReproduccionBase(BaseModel):

    tiempo_visto: int = Field(..., example=45, ge=1)
    id_perfil: uuid.UUID
    id_obra: uuid.UUID

    @validator("tiempo_visto")
    def validar_tiempo_visto(cls, v):
        if v <= 0:
            raise ValueError("El tiempo visto debe ser mayor a 0")
        return v


class HistorialReproduccionCreate(HistorialReproduccionBase):
    pass


class HistorialReproduccionUpdate(BaseModel):
    tiempo_visto: Optional[int]


class HistorialReproduccionResponse(HistorialReproduccionBase):
    id_historial: uuid.UUID
    fecha_visualizacion: datetime

    class Config:
        from_attributes = True
