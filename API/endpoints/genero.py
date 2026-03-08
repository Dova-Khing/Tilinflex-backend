"""
API de Genero - Endpoints para gestion de generos.
Define las rutas HTTP para consultar los generos disponibles
en la plataforma. Los generos son datos de solo lectura para
los usuarios, ya que son gestionados internamente por el sistema.
"""

from fastapi import APIRouter, Depends
from API.database.config import get_db
from sqlalchemy.orm import Session
from API.src.entities.generos import Genero
from API.schemas import GeneroResponse


router = APIRouter(
    prefix="/generos",
    tags=["Generos"]
)


@router.get("/", response_model=list[GeneroResponse])
def get_generos(db: Session = Depends(get_db)):
    """Retorna la lista de todos los generos disponibles en la plataforma."""
    generos = db.query(Genero).all()
    return generos
