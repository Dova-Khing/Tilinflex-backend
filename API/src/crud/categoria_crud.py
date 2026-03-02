"""
CRUD PARA CATEGORIA
La categoría se asigna a los audiovisuales para organizarlos y facilitar su búsqueda.
"""

from sqlalchemy.orm import Session
from API.src.entities.categoria import Categoria
from typing import List, Optional
from uuid import UUID


class CategoriaCRUD:
    def __init__(self, db: Session):
        self.db = db


    def obtener_categoria_por_nombre(self, categoria_nombre: str) -> Optional[Categoria]:
        """Obtener una categoría por nombre"""
        return self.db.query(Categoria).filter(Categoria.nombre_categoria == categoria_nombre).first()

    def obtener_categoria_por_id(self, categoria_id: UUID) -> Optional[Categoria]:
        """Obtener una categoría por ID"""
        return self.db.query(Categoria).filter(Categoria.id_categoria == categoria_id).first()

    def obtener_todas_categorias(self) -> List[Categoria]:
        """Obtener todas las categorías"""
        return self.db.query(Categoria).all()
