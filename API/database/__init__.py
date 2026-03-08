"""
Módulo de inicialización de base de datos
=========================================

Expone las funciones y objetos principales desde config.py
"""

from .config import engine, SessionLocal, get_db, DATABASE_URL
from ..src.crud.generos_crud import GeneroCRUD
from ..src.crud.categoria_crud import CategoriaCRUD
from sqlalchemy.orm import Session



CATEGORIAS_DEFAULT = [
    "Película",
    "Serie",
    "Documental",
    "Anime",
]

GENEROS_DEFAULT = [
    "Acción",
    "Drama",
    "Comedia",
    "Terror",
    "Ciencia ficción",
    "Aventura",
    "Romance",
    "Suspenso(Thriller)",
    "Fantasía",
    "Musical",
    "Documental",
]



__all__ = ["engine",
           "SessionLocal",
           "get_db",
             "DATABASE_URL"]



def inicializar_categorias(db: Session):
    crud = CategoriaCRUD(db)
    for nombre in CATEGORIAS_DEFAULT:
        if not crud.obtener_categoria_por_nombre(nombre):
            crud.crear_categoria(nombre)


def inicializar_generos(db: Session):
    crud = GeneroCRUD(db)
    for nombre in GENEROS_DEFAULT:
        if not crud.obtener_genero_por_nombre(nombre):
            crud.crear_genero(nombre)