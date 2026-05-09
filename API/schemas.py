"""
Modelos Pydantic para las respuestas y requests de la API.
Define los esquemas de validacion y serializacion para cada entidad
de la plataforma de streaming.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


# ------------------------------------
# USUARIO
# ------------------------------------

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
    fecha_registro: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    email: str
    contrasena: str


class CambioContrasena(BaseModel):
    contrasena_actual: str
    contrasena_nueva: str


# ------------------------------------
# PERFIL
# ------------------------------------

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
    id_perfil: UUID
    usuario_id: UUID
    fecha_registro: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


# ------------------------------------
# SUSCRIPCION
# ------------------------------------

class SuscripcionBase(BaseModel):
    tipo_suscripcion: str
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    id_detalle_suscripcion: Optional[UUID] = None


class SuscripcionCreate(SuscripcionBase):
    pass


class SuscripcionUpdate(BaseModel):
    tipo_suscripcion: Optional[str] = None
    fecha_fin: Optional[datetime] = None


class SuscripcionResponse(SuscripcionBase):
    id_suscripcion: UUID

    class Config:
        from_attributes = True


# ------------------------------------
# DETALLE SUSCRIPCION
# ------------------------------------

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


# ------------------------------------
# CATEGORIA
# ------------------------------------

class CategoriaResponse(BaseModel):
    id_categoria: UUID
    nombre_categoria: str

    class Config:
        from_attributes = True


# ------------------------------------
# GENERO
# ------------------------------------

class GeneroResponse(BaseModel):
    id_genero: UUID
    nombre_genero: str

    class Config:
        from_attributes = True


# ------------------------------------
# HISTORIAL REPRODUCCION
# ------------------------------------

class HistorialReproduccionBase(BaseModel):
    tiempo_visto: int
    fecha: datetime


class HistorialReproduccionCreate(HistorialReproduccionBase):
    id_perfil: UUID


class HistorialReproduccionUpdate(BaseModel):
    tiempo_visto: Optional[int] = None
    id_perfil: Optional[UUID] = None


class HistorialReproduccionResponse(HistorialReproduccionBase):
    id_historial: UUID
    id_perfil: UUID

    class Config:
        from_attributes = True


# ------------------------------------
# OBRAS
# ------------------------------------

class ObraCreate(BaseModel):
    mal_id: Optional[int] = None
    nombre: str
    nombre_japones: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    episodios: Optional[int] = None
    anio: Optional[int] = None
    temporada: Optional[str] = None
    estado: Optional[str] = None
    puntuacion: Optional[float] = None
    rango: Optional[int] = None
    duracion: Optional[str] = None
    estudios: Optional[str] = None
    generos_externos: Optional[str] = None
    thumbnail_url: Optional[str] = None
    banner_url: Optional[str] = None
    trailer_url: Optional[str] = None
    id_categoria: Optional[UUID] = None
    id_genero: Optional[UUID] = None


class ObraUpdate(BaseModel):
    nombre: Optional[str] = None
    nombre_japones: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    episodios: Optional[int] = None
    anio: Optional[int] = None
    temporada: Optional[str] = None
    estado: Optional[str] = None
    puntuacion: Optional[float] = None
    rango: Optional[int] = None
    duracion: Optional[str] = None
    estudios: Optional[str] = None
    generos_externos: Optional[str] = None
    thumbnail_url: Optional[str] = None
    banner_url: Optional[str] = None
    trailer_url: Optional[str] = None
    id_categoria: Optional[UUID] = None
    id_genero: Optional[UUID] = None


class ObraResponse(ObraCreate):
    id_obra: UUID
    fecha_registro: Optional[datetime] = None

    class Config:
        from_attributes = True


# ------------------------------------
# MODELOS CON RELACIONES
# ------------------------------------

class UsuarioConSuscripcion(UsuarioResponse):
    suscripcion: Optional[SuscripcionResponse] = None


class UsuarioConPerfil(UsuarioResponse):
    perfil: Optional[PerfilResponse] = None


class SuscripcionConDetalle(SuscripcionResponse):
    detalle_suscripcion: Optional[DetalleSuscripcionResponse] = None


class SuscripcionConUsuario(SuscripcionResponse):
    usuario: Optional[UsuarioResponse] = None


class DetalleConSuscripcion(DetalleSuscripcionResponse):
    suscripcion: Optional[SuscripcionResponse] = None


class CategoriaConObras(CategoriaResponse):
    obras: Optional[list[ObraResponse]] = None


class GeneroConObras(GeneroResponse):
    obras: Optional[list[ObraResponse]] = None


class ObraConCategoria(ObraResponse):
    categoria: Optional[CategoriaResponse] = None


class ObraConGenero(ObraResponse):
    genero: Optional[GeneroResponse] = None


class PerfilConUsuario(PerfilResponse):
    usuario: Optional[UsuarioResponse] = None


class PerfilConHistorial(PerfilResponse):
    historial: Optional[list[HistorialReproduccionResponse]] = None


class HistorialConPerfil(HistorialReproduccionResponse):
    perfil: Optional[PerfilResponse] = None


# ------------------------------------
# RESPUESTAS GENERICAS
# ------------------------------------

class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None


class RespuestaError(BaseModel):
    mensaje: str
    exito: bool = False
    error: str
    codigo: int
