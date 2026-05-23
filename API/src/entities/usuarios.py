from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID

from API.database.config import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre: str = Column(String(50), nullable=False)
    apellido: str = Column(String(50), nullable=False)
    email: str = Column(String(100), unique=True, nullable=False)
    telefono: Optional[str] = Column(String(20), nullable=True)
    edad: int = Column(Integer, nullable=True)
    contrasena_hash: str = Column(String(255), nullable=False)
    fecha_registro: datetime = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    admin: bool = Column(Boolean, default=False)
    pais: Optional[str] = Column(String(50), nullable=True)
    activo: bool = Column(Boolean, default=True)
    ultima_conexion: Optional[datetime] = Column(DateTime, nullable=True)

    perfiles = relationship("Perfil", back_populates="usuario", cascade="all, delete-orphan")
    suscripcion = relationship("Suscripcion", back_populates="usuario", uselist=False, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Usuario(id_usuario={self.id_usuario}, nombre='{self.nombre}', email='{self.email}')>"

    def to_dict(self) -> dict:
        return {
            "id_usuario": str(self.id_usuario),
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "edad": self.edad,
            "fecha_registro": self.fecha_registro.isoformat(),
            "fecha_actualizacion": self.fecha_actualizacion.isoformat(),
            "admin": self.admin,
            "pais": self.pais,
            "activo": self.activo,
        }
