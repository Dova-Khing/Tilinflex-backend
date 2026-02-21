"""
CRUD PARA GENERO
El género se asigna a las obras para clasificarlas y facilitar su búsqueda.
"""

from sqlalchemy.orm import Session
from entities.generos import Genero
from typing import List, Optional
from uuid import UUID


class GeneroCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_genero(self, nombre_genero: str) -> Genero:
        """Crear un nuevo género"""
        nuevo_genero = Genero(nombre_genero=nombre_genero)

        self.db.add(nuevo_genero)
        self.db.commit()
        self.db.refresh(nuevo_genero)

        return nuevo_genero

    def obtener_genero_por_id(self, genero_id: UUID) -> Optional[Genero]:
        """Obtener un género por ID"""
        return self.db.query(Genero).filter(Genero.id_genero == genero_id).first()

    def obtener_genero_por_nombre(self, nombre_genero: str) -> Optional[Genero]:
        """Obtener un género por nombre"""
        return (
            self.db.query(Genero).filter(Genero.nombre_genero == nombre_genero).first()
        )

    def obtener_todos_generos(self) -> List[Genero]:
        """Obtener todos los géneros"""
        return self.db.query(Genero).all()

    def actualizar_genero(self, genero_id: UUID, nuevo_nombre: str) -> Optional[Genero]:
        """Actualizar un género"""

        genero = self.obtener_genero_por_id(genero_id)

        if not genero:
            return None

        genero.nombre_genero = nuevo_nombre

        self.db.commit()
        self.db.refresh(genero)

        return genero

    def eliminar_genero(self, genero_id: UUID) -> bool:
        """Eliminar un género"""

        genero = self.obtener_genero_por_id(genero_id)

        if not genero:
            return False

        self.db.delete(genero)
        self.db.commit()

        return True
