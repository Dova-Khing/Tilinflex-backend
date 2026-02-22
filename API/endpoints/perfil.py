"""
API de Perfil - Endpoints para gestión de perfiles de usuarios

"""


from uuid import UUID

from src.crud.perfil_crud import validaciones_perfil
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import PerfilResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/perfil", tags=["Perfil"])

@router.get("/{nombre_usuario}", response_model=PerfilResponse)
async def validar_nombre(nombre_usuario: str, db: Session = Depends(get_db)):
    """
    Validar un perfil por nombre de usuario.

    Args:
        nombre_usuario (str): El nombre de usuario a validar.
    Returns:
        
    """
    try:
        crud = validaciones_perfil(db=db)
        perfiles = crud._validar_nombre_usuario(nombre_usuario=nombre_usuario)  
        if not perfiles:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado")
        return perfiles
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/usuario/{id_usuario}", response_model=PerfilResponse)
async def validar_id_usuario(id_usuario: UUID, db: Session = Depends(get_db)):
    """
    Validar un perfil por ID de usuario.

    Args:
        id_usuario (UUID): El ID de usuario a validar.
    Returns:
        PerfilResponse: El perfil asociado al ID de usuario.
    """
    try:
        crud = validaciones_perfil(db=db)
        perfiles = crud._validar_id_usuario(id_usuario=id_usuario)  
        if not perfiles:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil no encontrado")
        return perfiles
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    