"""
ENTIDAD DETALLE_SUSCRIPCION
MODELO DE DATOS PARA LA ENTIDAD DETALLE_SUSCRIPCION
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class DetalleSuscripcion(Base):
    """
    Modelo de DetalleSuscripcion que representa la tabla 'detalle_suscripcion'

    Atributos:
        id_detalle_suscripcion: Identificador único
        fecha_suscripcion: Fecha en la que se realizó el pago
        valor: Valor pagado
        metodo_pago: Método de pago utilizado
        id_suscripcion: FK hacia suscripcion
    """

    __tablename__ = 'detalle_suscripcion'

    id_detalle_suscripcion: uuid.UUID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    fecha_suscripcion: datetime = Column(
        DateTime,
        default=datetime.utcnow
    )

    valor = Column(
        Numeric(10, 2),
        nullable=False
    )

    metodo_pago: str = Column(
        String(50),
        nullable=False
    )

    # --------------------
    # FOREIGN KEY (One-to-One)
    # --------------------

    id_suscripcion: uuid.UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("suscripciones.id_suscripcion"),
        nullable=False,
        unique=True  # 🔥 importante para que sea 1:1
    )

    # --------------------
    # RELACION
    # --------------------

    suscripciones = relationship(
        "Suscripciones",
        back_populates="detalle_suscripcion"
    )

    def __repr__(self) -> str:
        return (
            f"<DetalleSuscripcion(id_detalle_suscripcion={self.id_detalle_suscripcion}, "
            f"valor={self.valor}, metodo_pago='{self.metodo_pago}')>"
        )

    def __to_dict__(self) -> dict:
        return {
            "id_detalle_suscripcion": str(self.id_detalle_suscripcion),
            "fecha_suscripcion": self.fecha_suscripcion.isoformat(),
            "valor": float(self.valor),
            "metodo_pago": self.metodo_pago,
            "id_suscripcion": str(self.id_suscripcion)
        }
"""
ESQUEMAS DE PYDANTIC PARA DETALLE_SUSCRIPCION
"""

class DetalleSuscripcionBase(BaseModel):

    valor: float = Field(..., example=29.99, gt=0)

    metodo_pago: str = Field(
        ...,
        example="tarjeta_credito"
    )

    id_suscripcion: uuid.UUID

    @validator('metodo_pago')
    def validar_metodo_pago(cls, v):
        metodos_validos = [
            "tarjeta_credito",
            "tarjeta_debito",
            "paypal",
            "transferencia"
        ]
        if v not in metodos_validos:
            raise ValueError(
                "Método de pago inválido"
            )
        return v
class DetalleSuscripcionCreate(DetalleSuscripcionBase):
    pass
class DetalleSuscripcionUpdate(BaseModel):
    valor: Optional[float]
    metodo_pago: Optional[str]

class DetalleSuscripcionResponse(DetalleSuscripcionBase):
    id_detalle_suscripcion: uuid.UUID
    fecha_suscripcion: datetime

    class Config:
        orm_mode = True
