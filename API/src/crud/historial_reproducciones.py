"""
CRUD PARA EL HISTORIAL DE LAS REPRODUCCIONES
El historial se genera automáticamente cuando el usuario reproduce una película,
no se crea ni se elimina manualmente desde este CRUD.
"""
from sqlalchemy.orm import Session
from entities.historial_reproduccion import HistorialReproducciones
from typing import List, Optional
from uuid import UUID


class HistorialReproduccionesCRUD:
    def __init__(self, db: Session):
        self.db = db

    def obtener_historial_por_usuario(self, id_usuario: UUID) -> List[HistorialReproducciones]:
        """Obtener el historial de reproducciones de un usuario"""
        return (
            self.db.query(HistorialReproducciones)
            .filter(HistorialReproducciones.id_usuario == id_usuario)
            .order_by(HistorialReproducciones.fecha_reproduccion.desc())
            .all()
        )

    def obtener_historial_por_video(self, id_usuario: UUID, id_video: UUID) -> Optional[HistorialReproducciones]:
        """Obtener un registro específico de historial para un usuario y video"""
        return (
            self.db.query(HistorialReproducciones)
            .filter(
                HistorialReproducciones.id_usuario == id_usuario,
                HistorialReproducciones.id_video == id_video
            )
            .first()
        )
