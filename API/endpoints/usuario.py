"""
API de Usuarios - Endpoints para gestión de usuarios

"""

from typing import List
from uuid import UUID

from ..src.crud.usuarios_crud import UsuarioCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import (
    CambioContrasena,
    RespuestaAPI,
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/", response_model=List[UsuarioResponse])
async def obtener_usuarios(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todos los usuarios registrados en el sistema.

    Parámetros:
        skip (int, opcional): Número de registros a omitir (para paginación). Default = 0.
        limit (int, opcional): Máximo de usuarios a retornar. Default = 100.
        db (Session): Sesión de base de datos proporcionada por la dependencia.

    Retorna:
        List[UsuarioResponse]: Lista de usuarios registrados.

    """
    try:
        usuario_crud = UsuarioCRUD(db)
        usuarios = usuario_crud.obtener_usuarios(skip=skip, limit=limit)
        return usuarios
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios: {str(e)}",
        )


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """
    Obtener un usuario por su ID único.

    Parámetros:
        usuario_id (UUID): Identificador único del usuario.
        db (Session): Sesión de base de datos.

    Retorna:
        UsuarioResponse: Información detallada del usuario.

    """
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.obtener_usuario(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuario: {str(e)}",
        )


@router.get("/email/{email}", response_model=UsuarioResponse)
async def obtener_usuario_por_email(email: str, db: Session = Depends(get_db)):
    """
     Obtener un usuario a partir de su dirección de correo electrónico.

    Parámetros:
        email (str): Correo electrónico del usuario a buscar.
        db (Session): Sesión de base de datos.

    Retorna:
        UsuarioResponse: Información del usuario asociado al correo.

    """
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.obtener_usuario_por_email(email)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuario: {str(e)}",
        )


@router.get("/username/{nombre_usuario}", response_model=UsuarioResponse)
async def obtener_usuario_por_nombre_usuario(
    nombre_usuario: str, db: Session = Depends(get_db)
):
    """
     Obtener un usuario por su nombre de usuario (username).

    Parámetros:
        nombre_usuario (str): Nombre de usuario a buscar.
        db (Session): Sesión de base de datos.

    Retorna:
        UsuarioResponse: Información del usuario.

    """
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.obtener_usuario_por_nombre_usuario(nombre_usuario)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuario: {str(e)}",
        )


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """
      Crear un nuevo usuario en el sistema.

    Parámetros (body):
        usuario_data (UsuarioCreate): Datos necesarios para crear un usuario:
            - nombre (str)
            - apellido (str)
            - email (str)
            - contraseña (str)
            - telefono (str)
            - edad (int)
            - pais (str)
            - es_admin (bool)

        db (Session): Sesión de base de datos.

    Retorna:
        UsuarioResponse: Datos del usuario recién creado.

    """
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.crear_usuario(
            nombre=usuario_data.nombre,
            apellido=usuario_data.apellido,
            email=usuario_data.email,
            contrasena=usuario_data.contrasena,
            telefono=usuario_data.telefono,
            edad=usuario_data.edad,
            pais=usuario_data.pais,
            es_admin=usuario_data.es_admin,
        )
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear usuario: {str(e)}",
        )


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(
    usuario_id: UUID, usuario_data: UsuarioUpdate, db: Session = Depends(get_db)
):
    """
    Actualizar la información de un usuario existente.

    Parámetros:
        usuario_id (UUID): Identificador único del usuario a actualizar.
        usuario_data (UsuarioUpdate): Campos opcionales a modificar.
        db (Session): Sesión de base de datos.

    Retorna:
        UsuarioResponse: Usuario actualizado con los cambios aplicados.
    """
    try:
        usuario_crud = UsuarioCRUD(db)

        usuario_existente = usuario_crud.obtener_usuario(usuario_id)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        campos_actualizacion = {
            k: v for k, v in usuario_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return usuario_existente

        usuario_actualizado = usuario_crud.actualizar_usuario(
            usuario_id, **campos_actualizacion
        )
        return usuario_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar usuario: {str(e)}",
        )


@router.delete("/{usuario_id}", response_model=RespuestaAPI)
async def eliminar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """
      Eliminar un usuario del sistema.

    Parámetros:
        usuario_id (UUID): Identificador único del usuario a eliminar.
        db (Session): Sesión de base de datos.

    Retorna:
        RespuestaAPI: Confirmación de eliminación exitosa.

    """
    try:
        usuario_crud = UsuarioCRUD(db)

        usuario_existente = usuario_crud.obtener_usuario(usuario_id)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        eliminado = usuario_crud.eliminar_usuario(usuario_id)
        if eliminado:
            return RespuestaAPI(mensaje="Usuario eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar usuario",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar usuario: {str(e)}",
        )


@router.patch("/{usuario_id}/desactivar", response_model=UsuarioResponse)
async def desactivar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """
     Desactivar un usuario sin eliminarlo de la base de datos (soft delete).

    Parámetros:
        usuario_id (UUID): Identificador único del usuario a desactivar.
        db (Session): Sesión de base de datos.

    Retorna:
        UsuarioResponse: Información del usuario desactivado.

    """
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.desactivar_usuario(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al desactivar usuario: {str(e)}",
        )


@router.post("/{usuario_id}/cambiar-contrasena", response_model=RespuestaAPI)
async def cambiar_contrasena(
    usuario_id: UUID, cambio_data: CambioContrasena, db: Session = Depends(get_db)
):
    """
    Cambiar la contraseña de un usuario.

    Parámetros:
        usuario_id (UUID): Identificador único del usuario.
        cambio_data (CambioContraseña): Contiene la contraseña actual y la nueva contraseña.
        db (Session): Sesión de base de datos.

    Retorna:
        RespuestaAPI: Confirmación del cambio de contraseña.

    """

    try:
        usuario_crud = UsuarioCRUD(db)

        usuario_existente = usuario_crud.obtener_usuario(usuario_id)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        cambio_exitoso = usuario_crud.cambiar_contrasena(
            usuario_id, cambio_data.contrasena_actual, cambio_data.nueva_contrasena
        )

        if cambio_exitoso:
            return RespuestaAPI(mensaje="Contrasena cambiada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al cambiar contraseña",
            )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cambiar contraseña: {str(e)}",
        )


@router.get("/admin/lista", response_model=List[UsuarioResponse])
async def obtener_usuarios_admin(db: Session = Depends(get_db)):
    """
    Obtener todos los usuarios con rol de administrador.

    Parámetros:
        db (Session): Sesión de base de datos.

    Retorna:
        List[UsuarioResponse]: Lista de usuarios administradores.

    """
    try:
        usuario_crud = UsuarioCRUD(db)
        admins = usuario_crud.obtener_usuarios_admin()
        return admins
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener administradores: {str(e)}",
        )


@router.get("/{usuario_id}/es-admin", response_model=RespuestaAPI)
async def verificar_es_admin(usuario_id: UUID, db: Session = Depends(get_db)):
    """
    Verificar si un usuario tiene privilegios de administrador.

    Parámetros:
        usuario_id (UUID): Identificador único del usuario.
        db (Session): Sesión de base de datos.

    Retorna:
        RespuestaAPI: Mensaje y flag indicando si el usuario es admin.
    """
    try:
        usuario_crud = UsuarioCRUD(db)
        es_admin = usuario_crud.es_admin(usuario_id)
        return RespuestaAPI(
            mensaje=f"El usuario {'es' if es_admin else 'no es'} administrador",
            exito=True,
            datos={"es_admin": es_admin},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar administrador: {str(e)}",
        )