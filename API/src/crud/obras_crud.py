"CRUD PARA OBRAS"

from sqlalchemy.orm import Session
from entities.obras import Obra
from typing import List, Optional
from uuid import UUID


class ObraCRUD:

    def __init__(self, db: Session):
        self.db = db

        def crear_obra(
            self,
            nombre: str,
            descripcion: Optional[str],
            episodios: int,
            anio: int,
            id_categoria: UUID,
            id_genero: UUID,
        ) -> Obra:
            """Crear una nueva obra"""
            nueva_obra = Obra(
                nombre=nombre,
                descripcion=descripcion,
                episodios=episodios,
                anio=anio,
                id_categoria=id_categoria,
                id_genero=id_genero,
            )

            self.db.add(nueva_obra)
            self.db.commit()
            self.db.refresh(nueva_obra)

            return nueva_obra

    def obtener_obra_por_id(self, obra_id: UUID) -> Optional[Obra]:
        """Obtener una obra por ID"""
        return self.db.query(Obra).filter(Obra.id_obra == obra_id).first()

    def obtener_obra_por_nombre(self, nombre: str) -> Optional[Obra]:
        """Obtener una obra por nombre"""
        return self.db.query(Obra).filter(Obra.nombre == nombre).first()

    def obtener_todas_obras(self) -> List[Obra]:
        """Obtener todas las obras"""
        return self.db.query(Obra).all()

    def actualizar_obra(self, obra_id: UUID, datos_actualizar: dict) -> Optional[Obra]:
        """Actualizar una obra"""

        obra = self.obtener_obra_por_id(obra_id)

        if not obra:
            return None

        for key, value in datos_actualizar.items():
            setattr(obra, key, value)

        self.db.commit()
        self.db.refresh(obra)

        return obra

    # -----------------------------
    # DELETE
    # -----------------------------

    def eliminar_obra(self, obra_id: UUID) -> bool:
        """Eliminar una obra"""

        obra = self.obtener_obra_por_id(obra_id)

        if not obra:
            return False

        self.db.delete(obra)
        self.db.commit()

        return True
