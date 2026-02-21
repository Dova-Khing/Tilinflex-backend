"""
CRUD para suscripciones
"""
import re
from entities.suscripciones import Suscripcion, SuscripcionBase
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional



class SuscripcionCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_suscripcion(self, suscripcion_data: SuscripcionBase) -> Suscripcion:
        """Crear una nueva suscripción"""
        nueva_suscripcion = Suscripcion(**suscripcion_data.dict())
        self.db.add(nueva_suscripcion)
        self.db.commit()
        self.db.refresh(nueva_suscripcion)
        return nueva_suscripcion

    def obtener_suscripcion(self, suscripcion_id: UUID) -> Optional[Suscripcion]:
        """Obtener una suscripción por ID"""
        return self.db.query(Suscripcion).filter(Suscripcion.id_suscripcion == suscripcion_id).first()

    def obtener_todas_las_suscripciones(self) -> List[Suscripcion]:
        """Obtener todas las suscripciones"""
        return self.db.query(Suscripcion).all()

    def actualizar_suscripcion(self, suscripcion_id: UUID, actualizacion_data: SuscripcionBase) -> Optional[Suscripcion]:
        """Actualizar una suscripción existente"""
        suscripcion = self.obtener_suscripcion(suscripcion_id)
        if not suscripcion:
            print("Error: La suscripción no existe.")
            return None

        for key, value in actualizacion_data.dict(exclude_unset=True).items():
            setattr(suscripcion, key, value)
        self.db.commit()
        self.db.refresh(suscripcion)
        return suscripcion
