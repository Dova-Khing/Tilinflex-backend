"""
API de Perfil - Endpoints para gestion de perfiles de usuarios.
Define las rutas HTTP para consultar perfiles por nombre de usuario
o por ID de usuario en la plataforma.
"""

from uuid import UUID
from typing import List

from API.src.crud.perfil_crud import PerfilCRUD
from API.database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from API.schemas import PerfilResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/perfil", tags=["Perfil"])


@router.get("/", response_model=List[PerfilResponse])
async def obtener_todos_perfiles(db: Session = Depends(get_db)):
    """
    Obtener todos los perfiles registrados en la plataforma.

    Returns:
        Lista de perfiles.

    Raises:
        HTTPException 500: Si ocurre un error interno al obtener los perfiles.
    """
    try:
        crud = PerfilCRUD(db=db)
        return crud.obtener_todos()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener perfiles: {str(e)}"
        )


@router.get("/{perfil_id}", response_model=PerfilResponse)
async def obtener_perfil(perfil_id: UUID, db: Session = Depends(get_db)):
    """
    Obtener un perfil por su ID.

    Args:
        perfil_id: Identificador unico del perfil.

    Returns:
        Perfil correspondiente al ID proporcionado.

    Raises:
        HTTPException 404: Si no se encuentra el perfil.
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = PerfilCRUD(db=db)
        perfil = crud.obtener_perfil_por_id(perfil_id=perfil_id)
        if not perfil:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil no encontrado"
            )
        return perfil
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el perfil: {str(e)}"
        )


@router.get("/usuario/{id_usuario}", response_model=List[PerfilResponse])
async def obtener_perfiles_por_usuario(id_usuario: UUID, db: Session = Depends(get_db)):
    """
    Obtener todos los perfiles asociados a un usuario.

    Args:
        id_usuario: Identificador unico del usuario.

    Returns:
        Lista de perfiles asociados al usuario.

    Raises:
        HTTPException 404: Si no se encuentran perfiles para el usuario.
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = PerfilCRUD(db=db)
        perfiles = crud.obtener_perfiles_por_usuario(id_usuario=id_usuario)
        if not perfiles:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron perfiles para este usuario"
            )
        return perfiles
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los perfiles del usuario: {str(e)}"
        )
