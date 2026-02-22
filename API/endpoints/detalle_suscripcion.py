"""
API de detalle suscripcion - Endpoints para gestión de detalle de suscripciones

"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.config import get_db
from src.crud.detalle_suscripcion_crud import DetalleSuscripcionCRUD
from schemas import DetalleSuscripcionCreate, DetalleSuscripcionResponse

router = APIRouter(prefix="/detalle-suscripcion", tags=["Detalle Suscripcion"])


@router.post("/", response_model=DetalleSuscripcionResponse)
async def crear_detalle(
    detalle_data: DetalleSuscripcionCreate, db: Session = Depends(get_db)
):
    try:
        crud = DetalleSuscripcionCRUD(db=db)

        # Validar que no exista ya detalle para esa suscripción (1:1)
        existe = crud.obtener_por_suscripcion(
            suscripcion_id=detalle_data.id_suscripcion
        )

        if existe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esta suscripción ya tiene un detalle registrado",
            )

        nuevo = crud.crear_detalle_suscripcion(
            valor=detalle_data.valor,
            metodo_pago=detalle_data.metodo_pago,
            id_suscripcion=detalle_data.id_suscripcion,
        )

        return nuevo

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{detalle_id}", response_model=DetalleSuscripcionResponse)
async def obtener_por_id(detalle_id: UUID, db: Session = Depends(get_db)):
    try:
        crud = DetalleSuscripcionCRUD(db=db)
        detalle = crud.obtener_por_id(detalle_id=detalle_id)

        if not detalle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Detalle no encontrado"
            )

        return detalle

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/suscripcion/{id_suscripcion}", response_model=DetalleSuscripcionResponse)
async def obtener_por_suscripcion(id_suscripcion: UUID, db: Session = Depends(get_db)):
    try:
        crud = DetalleSuscripcionCRUD(db=db)
        detalle = crud.obtener_por_suscripcion(suscripcion_id=id_suscripcion)

        if not detalle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No existe detalle para esta suscripción",
            )

        return detalle

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[DetalleSuscripcionResponse])
async def obtener_todos(db: Session = Depends(get_db)):
    try:
        crud = DetalleSuscripcionCRUD(db=db)
        return crud.obtener_todos()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
