"""
API de Suscripción - Endpoints para gestión de suscripciones

"""

from typing import List
from uuid import UUID

from ..src.crud.suscripciones_crud import SuscripcionCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import SuscripcionCreate, suscripcionResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/suscripciones", tags=["Suscripciones"])

@router.get("/", response_model=List[suscripcionResponse])
async def obtener_todas_suscripciones(
    skip: int = 0, limit: int = 100, db=Depends(get_db)
):
    """
    Obtener una lista de suscripciones

    Args: 
    - **skip**: Número de registros a omitir (paginación)
    - **limit**: Número máximo de registros a retornar (paginación)

    Returns:
        Retorna una lista de suscripciones.
    Raises:
        HTTPException(500): Si ocurre un error al obtener las suscripciones.
    """
    try:
        crud = SuscripcionCRUD(db=db)
        return crud.obtener_todas_las_suscripciones(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener suscripciones: {str(e)}",
        )
    
@router.get("/{suscripcion_id}", response_model=suscripcionResponse)
async def obtener_suscripcion(suscripcion_id: UUID, db: Session = Depends(get_db)):
    """
    Obtener una suscripción por ID

    Args:
    - **suscripcion_id**: ID de la suscripción a obtener

    Returns:
        Retorna la suscripción correspondiente al ID proporcionado.
    Raises:
        HTTPException(404): Si no se encuentra la suscripción con el ID proporcionado.
        HTTPException(500): Si ocurre un error al obtener la suscripción.
    """
    try:
        crud = SuscripcionCRUD(db=db)
        suscripcion = crud.obtener_suscripcion(suscripcion_id)
        if not suscripcion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Suscripción no encontrada",
            )
        return suscripcion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la suscripción: {str(e)}",
        )
    
@router.post("/", response_model=suscripcionResponse, status_code=status.HTTP_201_CREATED)
async def crear_suscripcion(suscripcion: SuscripcionCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva suscripción

    Args:
    - **suscripcion**: Datos de la suscripción a crear

    Returns:
        Retorna la suscripción creada.
    Raises:
        HTTPException(500): Si ocurre un error al crear la suscripción.
    """
    try:
        crud = SuscripcionCRUD(db=db)
        return crud.crear_suscripcion(suscripcion)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la suscripción: {str(e)}",
        )
    
@router.put("/{suscripcion_id}", response_model=suscripcionResponse)
async def actualizar_suscripcion(suscripcion_id: UUID, suscripcion: SuscripcionCreate, db: Session = Depends(get_db)):
    """
    Actualizar una suscripción existente

    Args:
    - **suscripcion_id**: ID de la suscripción a actualizar
    - **suscripcion**: Datos de la suscripción a actualizar

    Returns:
        Retorna la suscripción actualizada.
    Raises:
        HTTPException(404): Si no se encuentra la suscripción con el ID proporcionado.
        HTTPException(500): Si ocurre un error al actualizar la suscripción.
    """
    try:
        crud = SuscripcionCRUD(db=db)
        suscripcion_existente = crud.obtener_suscripcion(suscripcion_id)
        
        if not suscripcion_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Suscripción no encontrada",
            )
        
        campos = {k: v for k, v in suscripcion.dict().items() if v is not None}
        return crud.actualizar_suscripcion(suscripcion_id, campos)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la suscripción: {str(e)}",
        )