"""
CRUD PARA GENERO
El género se asigna a las obras para clasificarlas y facilitar su búsqueda.
"""

from sqlalchemy.orm import Session
from API.src.entities.generos import Genero
from typing import List, Optional
from uuid import UUID


class GeneroCRUD:
    def __init__(self, db: Session):
        self.db = db


    def obtener_genero_por_id(self, genero_id: UUID) -> Optional[Genero]:
        """Obtener un género por ID"""
        return self.db.query(Genero).filter(Genero.id_genero == genero_id).first()

    def obtener_genero_por_nombre(self, nombre_genero: str) -> Optional[Genero]:
        """Obtener un género por nombre"""
        return self.db.query(Genero).filter(Genero.nombre_genero == nombre_genero).first()

    def obtener_todos_generos(self) -> List[Genero]:
        """Obtener todos los géneros"""
        return self.db.query(Genero).all()
    
    def crear_genero(self, nombre: str) -> Genero:
        """Crear una nueva categoría"""
        genero = Genero(nombre_genero=nombre)
        self.db.add(genero)
        self.db.commit()
        self.db.refresh(genero)
        return genero
