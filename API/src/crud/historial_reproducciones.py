"""
CRUD PARA EL HISTORIAL DE LAS REPRODUCCIONES
"""

from sqlalchemy.orm import Session
from entities.historial_reproduccion import HistorialReproduccion
from typing import List, Optional
from uuid import UUID


class HistorialReproduccionCRUD:

    def __init__(self, db: Session):
        self.db = db

    # ---------------------------------
    # CREATE
    # ---------------------------------

    def crear_historial(
        self, tiempo_visto: int, id_perfil: UUID, id_obra: UUID
    ) -> HistorialReproduccion:
        """Crear un nuevo registro de historial"""

        nuevo_historial = HistorialReproduccion(
            tiempo_visto=tiempo_visto, id_perfil=id_perfil, id_obra=id_obra
        )

        self.db.add(nuevo_historial)
        self.db.commit()
        self.db.refresh(nuevo_historial)

        return nuevo_historial

    # ---------------------------------
    # READ
    # ---------------------------------

    def obtener_por_id(self, historial_id: UUID) -> Optional[HistorialReproduccion]:
        """Obtener historial por ID"""

        return (
            self.db.query(HistorialReproduccion)
            .filter(HistorialReproduccion.id_historial == historial_id)
            .first()
        )

    def obtener_por_perfil(self, perfil_id: UUID) -> List[HistorialReproduccion]:
        """Obtener historial por perfil"""

        return (
            self.db.query(HistorialReproduccion)
            .filter(HistorialReproduccion.id_perfil == perfil_id)
            .all()
        )

    def obtener_por_obra(self, obra_id: UUID) -> List[HistorialReproduccion]:
        """Obtener historial por obra"""

        return (
            self.db.query(HistorialReproduccion)
            .filter(HistorialReproduccion.id_obra == obra_id)
            .all()
        )

    def obtener_todos(self) -> List[HistorialReproduccion]:
        """Obtener todos los registros"""

        return self.db.query(HistorialReproduccion).all()

    # ---------------------------------
    # UPDATE
    # ---------------------------------

    def actualizar_historial(
        self, historial_id: UUID, datos_actualizar: dict
    ) -> Optional[HistorialReproduccion]:
        """Actualizar historial (ej: progreso de visualización)"""

        historial = self.obtener_por_id(historial_id)

        if not historial:
            return None

        for key, value in datos_actualizar.items():
            setattr(historial, key, value)

        self.db.commit()
        self.db.refresh(historial)

        return historial
