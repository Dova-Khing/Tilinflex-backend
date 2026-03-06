"""
API de Detalle Suscripcion - Endpoints para gestion de detalle de suscripciones.
Define las rutas HTTP para crear y consultar los detalles asociados
a cada suscripcion en la plataforma. Cada suscripcion solo puede tener
un detalle registrado.
"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from API.database.config import get_db
from API.src.crud.detalle_suscripcion_crud import DetalleSuscripcionCRUD
from API.schemas import DetalleSuscripcionCreate, DetalleSuscripcionResponse

router = APIRouter(prefix="/detalle-suscripcion", tags=["Detalle Suscripcion"])


@router.post("/", response_model=DetalleSuscripcionResponse, status_code=status.HTTP_201_CREATED)
async def crear_detalle(
    detalle_data: DetalleSuscripcionCreate, db: Session = Depends(get_db)
):
    """
    Crear un nuevo detalle de suscripcion.
    Cada suscripcion solo puede tener un detalle registrado.

    Args:
        detalle_data: Datos del detalle de suscripcion a crear.

    Returns:
        Detalle de suscripcion creado.

    Raises:
        HTTPException 400: Si ya existe un detalle para la suscripcion.
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = DetalleSuscripcionCRUD(db=db)

        existe = crud.obtener_por_suscripcion(
            suscripcion_id=detalle_data.id_suscripcion
        )

        if existe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esta suscripcion ya tiene un detalle registrado",
            )

        return crud.crear_detalle_suscripcion(
            valor=detalle_data.valor,
            metodo_pago=detalle_data.metodo_pago,
            id_suscripcion=detalle_data.id_suscripcion,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el detalle: {str(e)}"
        )


@router.get("/", response_model=List[DetalleSuscripcionResponse])
async def obtener_todos(db: Session = Depends(get_db)):
    """
    Obtener todos los detalles de suscripcion registrados.

    Returns:
        Lista de detalles de suscripcion.

    Raises:
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = DetalleSuscripcionCRUD(db=db)
        return crud.obtener_todos()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los detalles: {str(e)}"
        )


@router.get("/{detalle_id}", response_model=DetalleSuscripcionResponse)
async def obtener_por_id(detalle_id: UUID, db: Session = Depends(get_db)):
    """
    Obtener un detalle de suscripcion por su ID.

    Args:
        detalle_id: Identificador unico del detalle.

    Returns:
        Detalle de suscripcion correspondiente al ID.

    Raises:
        HTTPException 404: Si no se encuentra el detalle.
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = DetalleSuscripcionCRUD(db=db)
        detalle = crud.obtener_por_id(detalle_id=detalle_id)

        if not detalle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle no encontrado"
            )

        return detalle

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el detalle: {str(e)}"
        )


@router.get("/suscripcion/{id_suscripcion}", response_model=DetalleSuscripcionResponse)
async def obtener_por_suscripcion(id_suscripcion: UUID, db: Session = Depends(get_db)):
    """
    Obtener el detalle asociado a una suscripcion especifica.

    Args:
        id_suscripcion: Identificador unico de la suscripcion.

    Returns:
        Detalle de suscripcion asociado a la suscripcion.

    Raises:
        HTTPException 404: Si no existe detalle para la suscripcion.
        HTTPException 500: Si ocurre un error interno.
    """
    try:
        crud = DetalleSuscripcionCRUD(db=db)
        detalle = crud.obtener_por_suscripcion(suscripcion_id=id_suscripcion)

        if not detalle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No existe detalle para esta suscripcion",
            )

        return detalle

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el detalle de la suscripcion: {str(e)}"
        )
