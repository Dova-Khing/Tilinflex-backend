"""
Modelos Pydantic para las respuestas de la API
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


# Modelos base para Usuario
class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    edad: Optional[int] = None
    pais: Optional[str] = None
    admin: Optional[bool] = False
    activo: Optional[bool] = True

class UsuarioCreate(UsuarioBase):
    contrasena: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None



class UsuarioResponse(UsuarioBase):
    id_usuario: UUID
    id_suscripcion: Optional[UUID] = None
    fecha_registro: datetime
    fecha_actualizacion: datetime


    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    nombre_usuario: str
    contrasena: str


class CambioContrasena(BaseModel):
    contrasena_actual: str
    contrasena_nueva: str



# Modelos base para perfil
class PerfilBase(BaseModel):
    avatar_url: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    genero: Optional[str] = None
    intereses: Optional[str] = None

class PerfilCreate(PerfilBase):
    usuario_id: UUID


class PerfilUpdate(BaseModel):
    avatar_url: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = None
    genero: Optional[str] = None
    intereses: Optional[str] = None
    usuario_id: Optional[UUID] = None


class PerfilResponse(PerfilBase):
    id: UUID
    usuario_id: UUID
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


# Modelos base para suscripciones

class suscripcionBase(BaseModel):
    tipo: str
    costo: float
    duracion_dias: int



class suscripcionCreate(suscripcionBase):
    creado_por: str


class PartidaUpdate(BaseModel):
    costo_apuesta: Optional[float] = None
    estado: Optional[str] = None
    usuario_id: Optional[UUID] = None
    juego_id: Optional[UUID] = None
    premio_id: Optional[UUID] = None


class PartidaResponse(PartidaBase):
    id: UUID
    usuario_id: UUID
    juego_id: UUID
    premio_id: Optional[UUID] = None
    fecha: datetime

    class Config:
        from_attributes = True


# Modelos base para Juego
class JuegoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    costo_base: float


class JuegoCreate(JuegoBase):
    creado_por: str


class JuegoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    costo_base: Optional[float] = None
    creado_por: Optional[str] = None
    actualizado_por: Optional[str] = None


class JuegoResponse(JuegoBase):
    id: UUID
    fecha_registro: datetime
    fecha_actualizacion: datetime
    creado_por: str
    actualizado_por: Optional[str] = None

    class Config:
        from_attributes = True


# Modelos base para HistorialSaldo
class HistorialSaldoBase(BaseModel):
    tipo: str  # recarga, apuesta, premio
    monto: float


class HistorialSaldoCreate(HistorialSaldoBase):
    usuario_id: UUID


class HistorialSaldoUpdate(BaseModel):
    tipo: Optional[str] = None
    monto: Optional[float] = None
    usuario_id: Optional[UUID] = None


class HistorialSaldoResponse(HistorialSaldoBase):
    id: UUID
    usuario_id: UUID
    fecha: datetime

    class Config:
        from_attributes = True


# Modelos base para Boleto
class BoletoBase(BaseModel):
    numeros: str
    costo: float


class BoletoCreate(BoletoBase):
    usuario_id: UUID
    juego_id: UUID
    creado_por: str


class BoletoUpdate(BaseModel):
    numeros: Optional[str] = None
    costo: Optional[float] = None
    usuario_id: Optional[UUID] = None
    juego_id: Optional[UUID] = None
    actualizado_por: Optional[str] = None


class BoletoResponse(BoletoBase):
    id: UUID
    usuario_id: UUID
    juego_id: UUID
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None
    creado_por: str
    actualizado_por: Optional[str] = None

    class Config:
        from_attributes = True


# Modelos de respuesta con relaciones
class UsuarioConPartidas(UsuarioResponse):
    partidas: list[PartidaResponse] = []


class UsuarioConBoletos(UsuarioResponse):
    boletos: list[BoletoResponse] = []


class UsuarioConHistorialSaldo(UsuarioResponse):
    historial_saldo: list[HistorialSaldoResponse] = []


class PremioConJuego(PremioResponse):
    juego: JuegoResponse


class PartidaConUsuario(PartidaResponse):
    usuario: UsuarioResponse


class PartidaConJuego(PartidaResponse):
    juego: JuegoResponse


class JuegoConPartidas(JuegoResponse):
    partidas: list[PartidaResponse] = []


class JuegoConBoletos(JuegoResponse):
    boletos: list[BoletoResponse] = []


class HistorialSaldoConUsuario(HistorialSaldoResponse):
    usuario: UsuarioResponse


# Boleto con relaciones
class BoletoConUsuario(BoletoResponse):
    usuario: UsuarioResponse


class BoletoConJuego(BoletoResponse):
    juego: JuegoResponse


# Modelos de respuesta para la API
class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None


class RespuestaError(BaseModel):
    mensaje: str
    exito: bool = False
    error: str
    codigo: int
