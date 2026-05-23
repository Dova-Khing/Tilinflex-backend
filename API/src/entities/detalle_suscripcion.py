from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID

from API.database.config import Base


class DetalleSuscripcion(Base):
    __tablename__ = "detalle_suscripcion"

    id_detalle_suscripcion: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha_suscripcion: datetime = Column(DateTime, default=datetime.utcnow)
    valor = Column(Numeric(10, 2), nullable=False)
    metodo_pago: str = Column(String(50), nullable=False)

    id_suscripcion: uuid.UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("suscripciones.id_suscripcion"),
        nullable=False,
        unique=True,
    )

    suscripcion = relationship("Suscripcion", back_populates="detalle_suscripcion")

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
            "id_suscripcion": str(self.id_suscripcion),
        }
