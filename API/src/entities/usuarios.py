"""
ENTIDAD USUARIO

MODELO DE USUARIOS CON SQLAlchemy y esquemas de validacion con Pydantic.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
import uuid
from sqlalchemy.dialects.postgresql import UUID

from API.database.config import Base


class Usuario(Base):
    """
    Modelo de Usuario que representa la tabla 'usuarios'
    """

    __tablename__ = "usuarios"

    id_usuario: uuid.UUID = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nombre: str = Column(String(50), nullable=False)
    apellido: str = Column(String(50), nullable=False)
    email: str = Column(String(100), unique=True, nullable=False)
    telefono: Optional[str] = Column(String(20), nullable=True)
    edad: int = Column(Integer, nullable=True)
    contrasena_hash: str = Column(String(255), nullable=False)
    fecha_registro: datetime = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion: datetime = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    admin: bool = Column(Boolean, default=False)
    pais: Optional[str] = Column(String(50), nullable=True)
    activo: bool = Column(Boolean, default=True)

    perfil = relationship("Perfil", back_populates="usuario", uselist=False)
    suscripcion = relationship("Suscripcion", back_populates="usuario", uselist=False)

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


"""
ESQUEMA DE USUARIOS
"""


class UsuarioBase(BaseModel):
    nombre: str = Field(..., max_length=50)
    apellido: str = Field(..., max_length=50)
    email: EmailStr = Field(...)
    telefono: Optional[str] = Field(None, max_length=20)
    edad: Optional[int] = Field(None, ge=0)
    pais: Optional[str] = Field(None, max_length=50)
    activo: Optional[bool] = Field(None)
    admin: Optional[bool] = Field(None)


class UsuarioCreate(UsuarioBase):
    contrasena: str = Field(..., min_length=8)
    activo: bool = Field(default=True)
    admin: bool = Field(default=False)

    @validator("nombre", "apellido")
    def validar_nombre_apellido(cls, valor):
        if not valor.strip():
            raise ValueError("El nombre o apellido no puede estar vacío")
        return valor.strip()

    @validator("edad")
    def validar_edad(cls, valor):
        if valor is not None and valor <= 0:
            raise ValueError("La edad no puede ser negativa ni cero")
        return valor

    @validator("contrasena")
    def validar_contrasena(cls, valor):
        if len(valor) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return valor


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=50)
    apellido: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = Field(None)
    telefono: Optional[str] = Field(None, max_length=20)
    edad: Optional[int] = Field(None, ge=0)
    contrasena: Optional[str] = Field(None, min_length=8)
    pais: Optional[str] = Field(None, max_length=50)
    activo: Optional[bool] = Field(None)
    admin: Optional[bool] = Field(None)


class UsuarioResponse(UsuarioBase):
    id_usuario: uuid.UUID
    fecha_registro: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


class UsuarioListResponse(BaseModel):
    usuarios: List[UsuarioResponse]
    total: int
    pagina: int
    por_pagina: int

    class Config:
        from_attributes = True
