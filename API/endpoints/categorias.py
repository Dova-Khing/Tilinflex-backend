"""
API de categorias - Endpoints para gestión de categorias

"""

from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from src.entities.categoria import Categoria
from schemas import CategoriaResponse



router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"])


@router.get("/", response_model=list[CategoriaResponse])
def get_categorias(db: Session = Depends(get_db)):
    categoria = db.query(Categoria).all()
    return categoria
