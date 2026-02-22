"""
API de Historial de Reproducción - Endpoints para gestión del historial de reproducción

"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from database import get_db
from src.crud.historial_reproducciones import HistorialReproduccionCRUD
from schemas import (
    HistorialReproduccionCreate,
    HistorialReproduccionUpdate,
    HistorialReproduccionResponse,
)

router = APIRouter(prefix="/historial", tags=["Historial Reproducción"])


@router.post("/", response_model=HistorialReproduccionResponse)
def crear_historial(
    historial: HistorialReproduccionCreate, db: Session = Depends(get_db)
):
    crud = HistorialReproduccionCRUD(db)

    nuevo = crud.crear_historial(
        tiempo_visto=historial.tiempo_visto,
        id_perfil=historial.id_perfil,
        id_obra=historial.id_obra,
    )

    return nuevo


@router.get("/{historial_id}", response_model=HistorialReproduccionResponse)
def obtener_historial_por_id(historial_id: UUID, db: Session = Depends(get_db)):
    crud = HistorialReproduccionCRUD(db)
    historial = crud.obtener_por_id(historial_id)

    if not historial:
        raise HTTPException(status_code=404, detail="Historial no encontrado")

    return historial


@router.get("/perfil/{perfil_id}", response_model=List[HistorialReproduccionResponse])
def obtener_historial_por_perfil(perfil_id: UUID, db: Session = Depends(get_db)):
    crud = HistorialReproduccionCRUD(db)
    return crud.obtener_por_perfil(perfil_id)


@router.get("/obra/{obra_id}", response_model=List[HistorialReproduccionResponse])
def obtener_historial_por_obra(obra_id: UUID, db: Session = Depends(get_db)):
    crud = HistorialReproduccionCRUD(db)
    return crud.obtener_por_obra(obra_id)


@router.get("/", response_model=List[HistorialReproduccionResponse])
def obtener_todos(db: Session = Depends(get_db)):
    crud = HistorialReproduccionCRUD(db)
    return crud.obtener_todos()


@router.put("/{historial_id}", response_model=HistorialReproduccionResponse)
def actualizar_historial(
    historial_id: UUID,
    datos: HistorialReproduccionUpdate,
    db: Session = Depends(get_db),
):
    crud = HistorialReproduccionCRUD(db)

    historial_actualizado = crud.actualizar_historial(
        historial_id, datos.dict(exclude_unset=True)
    )

    if not historial_actualizado:
        raise HTTPException(status_code=404, detail="Historial no encontrado")

    return historial_actualizado
