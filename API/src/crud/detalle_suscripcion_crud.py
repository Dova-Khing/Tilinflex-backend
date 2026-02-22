"CRUD PARA detalle_suscripcion"

from sqlalchemy.orm import Session
from entities.detalle_suscripcion import DetalleSuscripcion
from typing import List, Optional
from uuid import UUID


class DetalleSuscripcionCRUD:

    def __init__(self, db: Session):
        self.db = db

    def crear_detalle_suscripcion(
        self, valor: float, metodo_pago: str, id_suscripcion: UUID
    ) -> DetalleSuscripcion:
        """Crear un nuevo detalle de suscripción"""

        nuevo_detalle = DetalleSuscripcion(
            valor=valor, metodo_pago=metodo_pago, id_suscripcion=id_suscripcion
        )

        self.db.add(nuevo_detalle)
        self.db.commit()
        self.db.refresh(nuevo_detalle)

        return nuevo_detalle

    # ---------------------------------
    # READ
    # ---------------------------------

    def obtener_por_id(self, detalle_id: UUID) -> Optional[DetalleSuscripcion]:
        """Obtener detalle por ID"""

        return (
            self.db.query(DetalleSuscripcion)
            .filter(DetalleSuscripcion.id_detalle_suscripcion == detalle_id)
            .first()
        )

    def obtener_por_suscripcion(
        self, suscripcion_id: UUID
    ) -> Optional[DetalleSuscripcion]:
        """Obtener detalle por ID de suscripción (1:1)"""

        return (
            self.db.query(DetalleSuscripcion)
            .filter(DetalleSuscripcion.id_suscripcion == suscripcion_id)
            .first()
        )

    def obtener_todos(self) -> List[DetalleSuscripcion]:
        """Obtener todos los detalles"""

        return self.db.query(DetalleSuscripcion).all()

    # ---------------------------------
    # UPDATE
    # ---------------------------------

    def actualizar_detalle(
        self, detalle_id: UUID, datos_actualizar: dict
    ) -> Optional[DetalleSuscripcion]:
        """Actualizar detalle de suscripción"""

        detalle = self.obtener_por_id(detalle_id)

        if not detalle:
            return None

        for key, value in datos_actualizar.items():
            setattr(detalle, key, value)

        self.db.commit()
        self.db.refresh(detalle)

        return detalle

    # ---------------------------------
    # DELETE
    # ---------------------------------

    def eliminar_detalle(self, detalle_id: UUID) -> bool:
        """Eliminar detalle de suscripción"""

        detalle = self.obtener_por_id(detalle_id)

        if not detalle:
            return False

        self.db.delete(detalle)
        self.db.commit()

        return True
