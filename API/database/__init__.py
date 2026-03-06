"""
Módulo de inicialización de base de datos
=========================================

Expone las funciones y objetos principales desde config.py
"""

from .config import engine, SessionLocal, get_db, DATABASE_URL
from API.src.entities.categoria import Categoria
from API.src.entities.generos import Genero

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



def init_categorias():
    db = SessionLocal()
    try:
       for nombre in CATEGORIAS_DEFAULT:
              existe =(
                   db.query(Categoria)
                     .filter(Categoria.nombre_categoria == nombre)
                        .first()
              )

              if not existe:
                    categoria = Categoria(nombre_categoria=nombre)
                    db.add(categoria)
                    db.commit()
    finally:
        db.close()


def init_generos():
    db = SessionLocal()
    try:
       for nombre in GENEROS_DEFAULT:
              existe =(
                   db.query(Genero)
                     .filter(Genero.nombre_genero == nombre)
                        .first()
              )

              if not existe:
                    genero = Genero(nombre_genero=nombre)
                    db.add(genero)
                    db.commit()
    finally:
        db.close()
