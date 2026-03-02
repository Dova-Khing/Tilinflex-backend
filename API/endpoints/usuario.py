"""
API de Usuarios - Endpoints para gestion de usuarios.
Define las rutas HTTP para crear, consultar, actualizar y eliminar
usuarios en la plataforma, incluyendo gestion de contrasenas y roles.
"""

from typing import List
from uuid import UUID

from API.src.crud.usuarios_crud import UsuarioCRUD
from API.database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from API.schemas import (
    CambioContrasena,
    RespuestaAPI,
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=List[UsuarioResponse])
async def obtener_usuarios(db: Session = Depends(get_db)):
    """
    Obtener todos los usuarios registrados en el sistema.

    Args:
        db: Sesion de base de datos.

    Returns:
        Lista de usuarios registrados.

    Raises:
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = UsuarioCRUD(db)
        return crud.obtener_todos_usuarios()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios: {str(e)}",
        )


@router.get("/admin/lista", response_model=List[UsuarioResponse])
async def obtener_usuarios_admin(db: Session = Depends(get_db)):
    """
    Obtener todos los usuarios con rol de administrador.

    Args:
        db: Sesion de base de datos.

    Returns:
        Lista de usuarios administradores.

    Raises:
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = UsuarioCRUD(db)
        return crud.obtener_usuarios_admin()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener administradores: {str(e)}",
        )


@router.get("/email/{email}", response_model=UsuarioResponse)
async def obtener_usuario_por_email(email: str, db: Session = Depends(get_db)):
    """
    Obtener un usuario por su correo electronico.

    Args:
        email: Correo electronico del usuario.
        db: Sesion de base de datos.

    Returns:
        Usuario asociado al correo.

    Raises:
        HTTPException 404: Si no se encuentra el usuario.
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = UsuarioCRUD(db)
        usuario = crud.obtener_usuario_por_email(email)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuario: {str(e)}",
        )


@router.get("/{usuario_id}/es-admin", response_model=RespuestaAPI)
async def verificar_es_admin(usuario_id: UUID, db: Session = Depends(get_db)):
    """
    Verificar si un usuario tiene privilegios de administrador.

    Args:
        usuario_id: Identificador unico del usuario.
        db: Sesion de base de datos.

    Returns:
        Mensaje indicando si el usuario es administrador.

    Raises:
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = UsuarioCRUD(db)
        es_admin = crud.es_admin(usuario_id)
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


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """
    Obtener un usuario por su ID.

    Args:
        usuario_id: Identificador unico del usuario.
        db: Sesion de base de datos.

    Returns:
        Usuario correspondiente al ID.

    Raises:
        HTTPException 404: Si no se encuentra el usuario.
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = UsuarioCRUD(db)
        usuario = crud.obtener_usuario(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
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

    Args:
        usuario_data: Datos del usuario a crear.
        db: Sesion de base de datos.

    Returns:
        Usuario creado.

    Raises:
        HTTPException 400: Si los datos son invalidos.
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = UsuarioCRUD(db)
        return crud.crear_usuario(
            nombre=usuario_data.nombre,
            apellido=usuario_data.apellido,
            email=usuario_data.email,
            contrasena=usuario_data.contrasena,
            telefono=usuario_data.telefono,
            edad=usuario_data.edad,
            pais=usuario_data.pais,
            admin=usuario_data.admin,
        )
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
    Actualizar la informacion de un usuario existente.

    Args:
        usuario_id: Identificador unico del usuario.
        usuario_data: Campos a modificar.
        db: Sesion de base de datos.

    Returns:
        Usuario actualizado.

    Raises:
        HTTPException 404: Si no se encuentra el usuario.
        HTTPException 400: Si los datos son invalidos.
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = UsuarioCRUD(db)
        usuario_existente = crud.obtener_usuario(usuario_id)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        campos = {k: v for k, v in usuario_data.dict().items() if v is not None}
        if not campos:
            return usuario_existente

        return crud.actualizar_usuario(usuario_id, **campos)
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

    Args:
        usuario_id: Identificador unico del usuario.
        db: Sesion de base de datos.

    Returns:
        Confirmacion de eliminacion.

    Raises:
        HTTPException 404: Si no se encuentra el usuario.
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = UsuarioCRUD(db)
        if not crud.obtener_usuario(usuario_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        if crud.eliminar_usuario(usuario_id):
            return RespuestaAPI(mensaje="Usuario eliminado exitosamente", exito=True)

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

    Args:
        usuario_id: Identificador unico del usuario.
        db: Sesion de base de datos.

    Returns:
        Usuario desactivado.

    Raises:
        HTTPException 404: Si no se encuentra el usuario.
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = UsuarioCRUD(db)
        usuario = crud.desactivar_usuario(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
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
    Cambiar la contrasena de un usuario.

    Args:
        usuario_id: Identificador unico del usuario.
        cambio_data: Contrasena actual y nueva contrasena.
        db: Sesion de base de datos.

    Returns:
        Confirmacion del cambio de contrasena.

    Raises:
        HTTPException 404: Si no se encuentra el usuario.
        HTTPException 400: Si la contrasena actual es incorrecta.
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = UsuarioCRUD(db)
        if not crud.obtener_usuario(usuario_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        if crud.cambiar_contrasena(
            usuario_id,
            cambio_data.contrasena_actual,
            cambio_data.contrasena_nueva
        ):
            return RespuestaAPI(mensaje="Contrasena cambiada exitosamente", exito=True)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al cambiar contrasena",
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cambiar contrasena: {str(e)}",
        )
