"""
ENTIDAD PERFIL
MODELO DE DATOS PARA LA ENTIDAD PERFIL
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy.dialects.postgresql import UUID

from API.database.config import Base


class Perfil(Base):
    """
    Modelo de Perfil que representa la tabla 'perfiles'

    Atributos:
        id_perfil: Identificador único
        nombre_usuario: Nombre del perfil
        idioma: Idioma del perfil
        es_infantil: Indica si es perfil infantil
        id_usuario: FK hacia usuario
    """

    __tablename__ = "perfiles"

    id_perfil: uuid.UUID = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    nombre_usuario: str = Column(String(100), nullable=False)

    idioma: str = Column(String(50), nullable=False, default="es")

    es_infantil: bool = Column(Boolean, default=False)

    fecha_creacion: datetime = Column(DateTime, default=datetime.utcnow)

    # --------------------
    # FOREIGN KEY
    # --------------------

    id_usuario: uuid.UUID = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )

    # --------------------
    # RELACIONES
    # --------------------

    usuario = relationship("Usuario", back_populates="perfil")

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
            "id_usuario": str(self.id_usuario),
            "idioma": self.idioma,
            "es_infantil": self.es_infantil,
            "fecha_creacion": self.fecha_creacion.isoformat(),
        }


"""
ESQUEMAS DE PYDANTIC PARA PERFIL
"""


class PerfilBase(BaseModel):

    nombre_usuario: str = Field(..., example="Camilo", min_length=2, max_length=100)

    idioma: str = Field(default="es", example="es")

    es_infantil: bool = Field(default=False, example=False)

    id_usuario: uuid.UUID

    @validator("idioma")
    def validar_idioma(cls, v):
        idiomas_validos = ["es", "en", "fr", "de"]
        if v not in idiomas_validos:
            raise ValueError("Idioma no soportado")
        return v


class PerfilCreate(PerfilBase):
    pass


class PerfilUpdate(BaseModel):
    nombre_usuario: Optional[str]
    idioma: Optional[str]
    es_infantil: Optional[bool]


class PerfilResponse(PerfilBase):
    id_perfil: uuid.UUID
    fecha_creacion: datetime

    class Config:
        orm_mode = True
