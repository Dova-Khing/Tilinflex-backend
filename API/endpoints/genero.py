"""
API de género - Endpoints para gestión de géneros

"""
from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from src.entities.generos import Genero
from schemas import GeneroResponse


router = APIRouter(
    prefix="/generos",
    tags=["Generos"])

@router.get("/", response_model=list[GeneroResponse])
def get_generos(db: Session = Depends(get_db)):
    genero = db.query(Genero).all()
    return genero
