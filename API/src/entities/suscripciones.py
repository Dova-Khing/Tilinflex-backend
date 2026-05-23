"""
ENTIDAD SUSCRIPCIONES
MODELO DE DATOS PARA LA ENTIDAD SUSCRIPCIONES
"""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID

from API.database.config import Base


class Suscripcion(Base):
    """
    Modelo de Suscripcion que representa la tabla 'suscripciones'
    Un usuario puede tener una suscripcion, que se crea cuando decide pagar.
    """

    __tablename__ = "suscripciones"

    id_suscripcion: uuid.UUID = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tipo_suscripcion: str = Column(String(50), nullable=False)
    fecha_inicio: datetime = Column(DateTime, default=datetime.utcnow)
    fecha_fin: datetime = Column(DateTime, nullable=True)

    # --------------------
    # FOREIGN KEY
    # --------------------

    id_usuario: uuid.UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("usuarios.id_usuario"),
        nullable=False,
        unique=True,  # Un usuario solo puede tener una suscripcion activa
    )

    # --------------------
    # RELACIONES
    # --------------------

    usuario = relationship("Usuario", back_populates="suscripcion")
    detalle_suscripcion = relationship(
        "DetalleSuscripcion", back_populates="suscripcion", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<Suscripcion(id_suscripcion={self.id_suscripcion}, "
            f"tipo_suscripcion='{self.tipo_suscripcion}')>"
        )

    def __to_dict__(self) -> dict:
        return {
            "id_suscripcion": str(self.id_suscripcion),
            "tipo_suscripcion": self.tipo_suscripcion,
            "fecha_inicio": self.fecha_inicio.isoformat(),
            "fecha_fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
            "id_usuario": str(self.id_usuario),
        }


"""
ESQUEMAS DE PYDANTIC PARA LA ENTIDAD SUSCRIPCIONES
"""


class SuscripcionBase(BaseModel):
    tipo_suscripcion: str = Field(..., example="mensual")
    fecha_inicio: Optional[datetime] = Field(default_factory=datetime.utcnow)
    fecha_fin: Optional[datetime] = Field(None)
    id_usuario: uuid.UUID

    @validator("tipo_suscripcion")
    def validate_tipo_suscripcion(cls, v):
        if v not in ["mensual", "anual", "trimestral"]:
            raise ValueError(
                "El tipo de suscripción debe ser 'mensual', 'anual' o 'trimestral'"
            )
        return v

    @validator("fecha_fin")
    def validate_fecha_fin(cls, v, values):
        if v and "fecha_inicio" in values and v < values["fecha_inicio"]:
            raise ValueError(
                "La fecha de fin no puede ser anterior a la fecha de inicio"
            )
        return v


class SuscripcionCreate(SuscripcionBase):
    pass


class SuscripcionUpdate(BaseModel):
    tipo_suscripcion: Optional[str] = Field(None)
    fecha_fin: Optional[datetime] = Field(None)


class SuscripcionResponse(SuscripcionBase):
    id_suscripcion: uuid.UUID

    class Config:
        from_attributes = True
