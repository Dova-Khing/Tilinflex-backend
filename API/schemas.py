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

class SuscripcionBase(BaseModel):
    tipo: str
    costo: float
    duracion_dias: int

class suscripcionResponse(SuscripcionBase):
    id_suscripcion: UUID
    id_detalle_suscripcion: Optional[UUID] = None

class SuscripcionCreate(SuscripcionBase):
    creado_por: str

#Modelos base para Detalle Suscripcion

class DetalleSuscripcionBase(BaseModel):
    valor: int
    metodo_pago: str
    fecha_suscripcion: datetime

class DetalleSuscripcionCreate(DetalleSuscripcionBase):
    id_suscripcion: UUID

class DetalleSuscripcionResponse(DetalleSuscripcionBase):
    id_detalle_suscripcion: UUID
    id_suscripcion: UUID

    class Config:
        from_attributes = True

#Modelos base para Categoria
class CategoriaResponse(BaseModel):
    id_categoria: UUID
    nombre_categoria: str

    class Config:
        from_attributes = True


# Modelos base para generos
class GeneroResponse(BaseModel):
    id_genero: UUID
    nombre_genero: str

    class Config:
        from_attributes = True

# Modelos base para HistorialReproduccion
class HistorialReproduccionBase(BaseModel):
    tiempo_visto: int
    fecha: datetime


class HistorialReproduccionCreate(HistorialReproduccionBase):
    id_perfil: UUID


class HistorialReproduccionUpdate(BaseModel):
    tiempo_visto: Optional[int] = None
    id_perfil: Optional[UUID] = None


class HistorialReproduccionResponse(HistorialReproduccionBase):
    id: UUID
    id_perfil: UUID
    fecha: datetime

    class Config:
        from_attributes = True


# Modelos base para Obras
class ObraBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    episodios: Optional[int] = None
    año: Optional[int] = None
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None


class ObraCreate(ObraBase):
    id_categoria: UUID
    id_genero: UUID


class ObrasUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    episodios: Optional[int] = None
    año: Optional[int] = None
    id_categoria: Optional[UUID] = None
    id_genero: Optional[UUID] = None


class ObraResponse(ObraBase):
    id: UUID
    id_categoria: UUID
    id_genero: UUID
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None
    creado_por: str
    actualizado_por: Optional[str] = None

    class Config:
        from_attributes = True


# Modelos de respuesta con relaciones
class UsuarioConSuscripcion(UsuarioResponse):
    suscripcion: Optional[SuscripcionCreate] = None

class UsuarioConPerfil(UsuarioResponse):
    perfil: Optional[PerfilResponse] = None

class SuscripcionConDetalle(suscripcionResponse):
    detalle_suscripcion: Optional[DetalleSuscripcionResponse] = None

class suscripcionConUsuario(suscripcionResponse):
    usuario: Optional[UsuarioResponse] = None

class detalleConSuscripcion(DetalleSuscripcionResponse):
    suscripcion: Optional[suscripcionResponse] = None

class categoriaConObras(CategoriaResponse):
    obras: Optional[list[ObraResponse]] = None

class generoConObras(GeneroResponse):
    obras: Optional[list[ObraResponse]] = None

class ObrasConCategoria(ObraResponse):
    categoria: Optional[CategoriaResponse] = None

class ObrasConGenero(ObraResponse):
    genero: Optional[GeneroResponse] = None

class perfilConUsuario(PerfilResponse):
    usuario: Optional[UsuarioResponse] = None

class perfilConHistorial(PerfilResponse):
    historial: Optional[list[HistorialReproduccionResponse]] = None

class historialConPerfil(HistorialReproduccionResponse):
    perfil: Optional[PerfilResponse] = None

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
