"""
API de Suscripcion - Endpoints para gestion de suscripciones.
Define las rutas HTTP para crear, consultar y actualizar suscripciones
de los usuarios en la plataforma.
"""

from typing import List
from uuid import UUID

from API.src.crud.suscripciones_crud import SuscripcionCRUD
from API.database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from API.schemas import SuscripcionCreate, SuscripcionResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/suscripciones", tags=["Suscripciones"])


@router.get("/", response_model=List[SuscripcionResponse])
async def obtener_todas_suscripciones(db: Session = Depends(get_db)):
    """
    Obtener una lista de todas las suscripciones.

    Returns:
        Lista de suscripciones registradas.

    Raises:
        HTTPException 500: Si ocurre un error interno al obtener las suscripciones.
    """
    try:
        crud = SuscripcionCRUD(db=db)
        return crud.obtener_todas_las_suscripciones()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener suscripciones: {str(e)}",
        )


@router.get("/{suscripcion_id}", response_model=SuscripcionResponse)
async def obtener_suscripcion(suscripcion_id: UUID, db: Session = Depends(get_db)):
    """
    Obtener una suscripcion por ID.

    Args:
        suscripcion_id: Identificador unico de la suscripcion.

    Returns:
        Suscripcion correspondiente al ID proporcionado.

    Raises:
        HTTPException 404: Si no se encuentra la suscripcion.
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = SuscripcionCRUD(db=db)
        suscripcion = crud.obtener_suscripcion(suscripcion_id)
        if not suscripcion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Suscripcion no encontrada",
            )
        return suscripcion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la suscripcion: {str(e)}",
        )


@router.post(
    "/", response_model=SuscripcionResponse, status_code=status.HTTP_201_CREATED
)
async def crear_suscripcion(
    suscripcion: SuscripcionCreate, db: Session = Depends(get_db)
):
    """
    Crear una nueva suscripcion.

    Args:
        suscripcion: Datos de la suscripcion a crear.

    Returns:
        Suscripcion creada.

    Raises:
        HTTPException 500: Si ocurre un error interno al crear la suscripcion.
    """
    try:
        crud = SuscripcionCRUD(db=db)
        return crud.crear_suscripcion(suscripcion)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la suscripcion: {str(e)}",
        )


@router.put("/{suscripcion_id}", response_model=SuscripcionResponse)
async def actualizar_suscripcion(
    suscripcion_id: UUID,
    suscripcion: SuscripcionCreate,
    db: Session = Depends(get_db),
):
    """
    Actualizar una suscripcion existente.

    Args:
        suscripcion_id: Identificador unico de la suscripcion a actualizar.
        suscripcion: Datos nuevos de la suscripcion.

    Returns:
        Suscripcion actualizada.

    Raises:
        HTTPException 404: Si no se encuentra la suscripcion.
        HTTPException 500: Si ocurre un error interno al actualizar la suscripcion.
    """
    try:
        crud = SuscripcionCRUD(db=db)
        suscripcion_existente = crud.obtener_suscripcion(suscripcion_id)

        if not suscripcion_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Suscripcion no encontrada",
            )

        return crud.actualizar_suscripcion(suscripcion_id, suscripcion)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la suscripcion: {str(e)}",
        )
