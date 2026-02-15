"""
ENTINDAD USUARIO

MODELO DE USUARIOS CON SQLAlchemy y esquemas de validacion con Pydantic.
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

class Usuario(Base):
    """
    Modelo de Usuario que representa la tabla 'usuarios'

    Atributos:
        id_usuario: Identificador único
        id_suscripcion FK: Identificador de suscripción (si aplica)
        nombre: Nombre completo
        apellido: Apellido
        email: Correo electrónico único
        telefono: Número telefónico
        edad: Edad del usuario
        contrasena_hash: Hash de la contraseña
        fecha_registro: Fecha de registro del usuario
        fecha_actualizacion: Fecha de última actualización del usuario
        admin: Indica si el usuario tiene privilegios de administrador
        pais: País de residencia
        activo: Indica si el usuario está activo
    """

__tablename__ = 'usuarios'

id_usuario: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
id_suscripcion:Optional [uuid.UUID] = Column(UUID(as_uuid=True), nullable=True)
nombre: str = Column(String(50), nullable=False)
apellido: str = Column(String(50), nullable=False)
email: EmailStr = Column(String(100), unique=True, nullable=False)
telefono: Optional[str] = Column(String(20), nullable=True)
edad: int = Column(Integer, nullable=True)
contrasena_hash: str = Column(String(255), nullable=False)
fecha_registro: datetime = Column(DateTime, default=datetime.utcnow)
fecha_actualizacion: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
admin: bool = Column(Boolean, default=False)
pais: Optional[str] = Column(String(50), nullable=True)
activo: bool = Column(Boolean, default=True)

pefil = relationship(
    "Perfil", back_populates="usuario", uselist=False)

suscripcion = relationship(
    "Suscripcion", back_populates="usuarios")


def __repr__(self) -> str:
        return f"<Usuario(id_usuario={self.id_usuario}, nombre='{self.nombre}', apellido='{self.apellido}', email='{self.email}')>"

def to_dict(self) -> dict:
        return {
            "id_usuario": str(self.id_usuario),
            "id_suscripcion": str(self.id_suscripcion) if self.id_suscripcion else None,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "edad": self.edad,
            "fecha_registro": self.fecha_registro.isoformat(),
            "fecha_actualizacion": self.fecha_actualizacion.isoformat(),
            "admin": self.admin,
            "pais": self.pais,
            "activo": self.activo
        }

"""
ESQUEMA DE USUARIOS
Esquema de validación para la creación y actualización de usuarios utilizando Pydantic.
"""

class UsuarioBase(BaseModel):
    """
    Esquema base para un usuario

    Atributos:
        nombre: Nombre completo del usuario
        apellido: Apellido del usuario
        email: Correo electrónico único
        telefono: Número telefónico (opcional)
        edad: Edad del usuario (opcional)
        pais: País de residencia (opcional)
        activo: Indica si el usuario está activo (opcional)
        admin: ¿Es administrador del sistema? (opcional)
    """
    nombre: str = Field(..., max_length=50, description="Nombre completo del usuario")
    apellido: str = Field(..., max_length=50, description="Apellido del usuario")
    email: EmailStr = Field(...)
    telefono: Optional[str] = Field(None, max_length=20, description="Número telefónico del usuario")
    edad: Optional[int] = Field(None, ge=0, description="Edad del usuario")
    pais: Optional[str] = Field(None, max_length=50, description="País de residencia del usuario")
    activo: Optional[bool] = Field(None, description="Indica si el usuario está activo")
    admin: Optional[bool] = Field(None, description="¿Es administrador del sistema?")

class UsuarioCreate(BaseModel):
    """
    Esquema para la creación de un nuevo usuario

    Atributos:
        nombre: Nombre completo del usuario
        apellido: Apellido del usuario
        email: Correo electrónico único
        telefono: Número telefónico (opcional)
        edad: Edad del usuario (opcional)
        contrasena: Contraseña en texto plano
        pais: País de residencia (opcional)
    """
    nombre: str = Field(..., max_length=50, description ="Nombre completo del usuario")
    apellido: str = Field(..., max_length=50, description="Apellido del usuario")
    email: EmailStr = Field(...)
    telefono: Optional[str] = Field(None, max_length=20, description="Número telefónico del usuario")
    edad: Optional[int] = Field(None, ge=0, description="Edad del usuario")
    contrasena: str = Field(..., min_length=8, description="Contraseña del usuario")
    pais: Optional[str] = Field(None, max_length=50, description="País de residencia del usuario")
    activo: bool = Field(default=True, description="Indica si el usuario está activo")
    admin: bool = Field(default=False, description="¿Es administrador del sistema?")


    @validator("nombre", "apellido")
    def validar_nombre_apellido(cls, valor):
        os.system("cls")
        if not valor.strip():
            raise ValueError("El nombre o apellido no puede estar vacío")
        return valor.strip()

    @validator("edad")
    def validar_edad(cls, valor):
        os.system("cls")
        if valor is not None and valor <= 0:
            raise ValueError("La edad no puede ser negativa ni cero")
        return valor

    @validator("contrasena")
    def validar_contrasena(cls, valor):
        os.system("cls")
        if len(valor) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return valor


class UsuarioCreate(UsuarioBase):
    """
    Esquema para la creación de un nuevo usuario, hereda de UsuarioBase

    Atributos adicionales:
        contrasena: Contraseña en texto plano
    """
    contrasena: str = Field(..., min_length=8, description="Contraseña del usuario")


class UsuarioUpdate(BaseModel):
    """
    Esquema para la actualización de un usuario existente

    Atributos:
        nombre: Nombre completo del usuario (opcional)
        apellido: Apellido del usuario (opcional)
        email: Correo electrónico único (opcional)
        telefono: Número telefónico (opcional)
        edad: Edad del usuario (opcional)
        contrasena: Contraseña en texto plano (opcional)
        pais: País de residencia (opcional)
        activo: Indica si el usuario está activo (opcional)
        admin: ¿Es administrador del sistema? (opcional)
    """
    nombre: Optional[str] = Field(None, max_length=50, )
    apellido: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = Field(None)
    telefono: Optional[str] = Field(None, max_length=20)
    edad: Optional[int] = Field(None, ge=0)
    contrasena: Optional[str] = Field(None, min_length=8)
    pais: Optional[str] = Field(None, max_length=50)
    activo: Optional[bool] = Field(None)
    admin: Optional[bool] = Field(None, min_length=9)


class UsuarioResponse(UsuarioBase):
    """
    Esquema para la respuesta de un usuario

    Atributos:
        id_usuario: Identificador único del usuario
        id_suscripcion: Identificador de suscripción (si aplica)

    """
    id_usuario: uuid.UUID
    id_suscripcion: Optional[uuid.UUID]
    fecha_registro
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        orm_mode = True
        json_encoders = {
            DateTime: lambda v: v.isoformat()}

class UsuarioListResponse(BaseModel):
    """
    Esquema para la respuesta de una lista de usuarios

    Atributos:
        usuarios: Lista de usuarios
    """
    usuarios: List[UsuarioResponse]
    total: int
    pagina: int
    por_pagina: int

    class Config:
         from_attributes = True
