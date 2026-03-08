"""
API de categorias - Endpoints para gestion de categorias.
Define las rutas HTTP para consultar las categorias disponibles
en la plataforma. Las categorias son datos de solo lectura para
los usuarios, ya que son gestionadas internamente por el sistema.
"""

from fastapi import APIRouter, Depends
from API.database.config import get_db
from sqlalchemy.orm import Session
from API.src.entities.categoria import Categoria
from API.schemas import CategoriaResponse


router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)


@router.get("/", response_model=list[CategoriaResponse])
def get_categorias(db: Session = Depends(get_db)):
    """Retorna la lista de todas las categorias disponibles en la plataforma."""
    categorias = db.query(Categoria).all()
    return categorias
