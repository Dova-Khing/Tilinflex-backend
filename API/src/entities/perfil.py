from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID

from API.database.config import Base


class Perfil(Base):
    __tablename__ = "perfiles"

    id_perfil: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_usuario: str = Column(String(100), nullable=False)
    avatar_url: str = Column(Text, nullable=True, default="av1")
    idioma: str = Column(String(50), nullable=False, default="es")
    es_infantil: bool = Column(Boolean, default=False)
    fecha_creacion: datetime = Column(DateTime, default=datetime.utcnow)

    id_usuario: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False)

    usuario = relationship("Usuario", back_populates="perfiles")
    historial_reproduccion = relationship(
        "HistorialReproduccion", back_populates="perfil", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return (
            f"<Perfil(id_perfil={self.id_perfil}, "
            f"nombre_usuario='{self.nombre_usuario}', "
            f"id_usuario={self.id_usuario})>"
        )

    def __to_dict__(self) -> dict:
        return {
            "id_perfil": str(self.id_perfil),
            "nombre_usuario": self.nombre_usuario,
            "avatar_url": self.avatar_url,
            "id_usuario": str(self.id_usuario),
            "idioma": self.idioma,
            "es_infantil": self.es_infantil,
            "fecha_creacion": self.fecha_creacion.isoformat(),
        }
