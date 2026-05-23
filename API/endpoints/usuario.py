from typing import List
from uuid import UUID

from API.src.crud.usuarios_crud import UsuarioCRUD
from API.database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from API.schemas import CambioContrasena, RespuestaAPI, UsuarioCreate, UsuarioResponse, UsuarioUpdate
from sqlalchemy.orm import Session
from API.dependencies import require_admin
from API.src.core.auth import get_current_user, CurrentUser

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=List[UsuarioResponse])
async def obtener_usuarios(
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_admin),
):
    try:
        return UsuarioCRUD(db).obtener_todos_usuarios()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/admin/lista", response_model=List[UsuarioResponse])
async def obtener_usuarios_admin(
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_admin),
):
    try:
        return UsuarioCRUD(db).obtener_usuarios_admin()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/email/{email}", response_model=UsuarioResponse)
async def obtener_usuario_por_email(
    email: str,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_admin),
):
    try:
        usuario = UsuarioCRUD(db).obtener_usuario_por_email(email)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{usuario_id}/es-admin", response_model=RespuestaAPI)
async def verificar_es_admin(usuario_id: UUID, db: Session = Depends(get_db)):
    try:
        es_admin = UsuarioCRUD(db).es_admin(usuario_id)
        return RespuestaAPI(
            mensaje=f"El usuario {'es' if es_admin else 'no es'} administrador",
            exito=True,
            datos={"es_admin": es_admin},
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    try:
        usuario = UsuarioCRUD(db).obtener_usuario(usuario_id)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(
    usuario_id: UUID,
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_admin),
):
    try:
        crud = UsuarioCRUD(db)
        campos = {k: v for k, v in usuario_data.dict().items() if v is not None}
        if not campos:
            usuario = crud.obtener_usuario(usuario_id)
            if not usuario:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
            return usuario
        resultado = crud.actualizar_usuario(usuario_id, **campos)
        if not resultado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return resultado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{usuario_id}", response_model=RespuestaAPI)
async def eliminar_usuario(
    usuario_id: UUID,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_admin),
):
    try:
        if not UsuarioCRUD(db).eliminar_usuario(usuario_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return RespuestaAPI(mensaje="Usuario eliminado exitosamente", exito=True)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{usuario_id}/desactivar", response_model=UsuarioResponse)
async def desactivar_usuario(
    usuario_id: UUID,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_admin),
):
    try:
        usuario = UsuarioCRUD(db).desactivar_usuario(usuario_id)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{usuario_id}/cambiar-contrasena", response_model=RespuestaAPI)
async def cambiar_contrasena(
    usuario_id: UUID,
    cambio_data: CambioContrasena,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.id_usuario != usuario_id and not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sin permiso para cambiar esta contraseña")
    try:
        resultado = UsuarioCRUD(db).cambiar_contrasena(
            usuario_id, cambio_data.contrasena_actual, cambio_data.contrasena_nueva
        )
        if not resultado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return RespuestaAPI(mensaje="Contraseña cambiada exitosamente", exito=True)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
