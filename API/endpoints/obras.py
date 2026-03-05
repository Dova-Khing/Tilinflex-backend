"""
API de Obras - Endpoints para gestión de obras
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from API.database.config import get_db
from API.dependencies import require_admin
from API.schemas import ObraCreate, ObraResponse
from API.src.crud.obras_crud import ObraCRUD


router = APIRouter(prefix="/obras", tags=["Obras"])


# Endpoints PÚBLICOS (todos pueden acceder)
@router.get("/", response_model=List[ObraResponse])
def obtener_obras(db: Session = Depends(get_db)):
    crud = ObraCRUD(db)
    return crud.obtener_todas_obras()


@router.get("/{obra_id}", response_model=ObraResponse)
def obtener_obra(obra_id: UUID, db: Session = Depends(get_db)):
    crud = ObraCRUD(db)
    obra = crud.obtener_obra_por_id(obra_id)
    if not obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")
    return obra


# Endpoints PROTEGIDOS (solo admin)
@router.post("/", response_model=ObraResponse)
def crear_obra(
    obra_data: ObraCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    crud = ObraCRUD(db)
    return crud.crear_obra(**obra_data.dict())


@router.put("/{obra_id}", response_model=ObraResponse)
def actualizar_obra(
    obra_id: UUID,
    obra_data: ObraCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    crud = ObraCRUD(db)
    obra = crud.actualizar_obra(obra_id, obra_data.dict())
    if not obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")
    return obra


@router.delete("/{obra_id}")
def eliminar_obra(
    obra_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    crud = ObraCRUD(db)
    if not crud.eliminar_obra(obra_id):
        raise HTTPException(status_code=404, detail="Obra no encontrada")
    return {"mensaje": "Obra eliminada"}
