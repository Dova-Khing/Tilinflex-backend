from sqlalchemy.orm import Session
from API.src.entities.obras import Obra
from typing import List, Optional
from uuid import UUID


class ObraCRUD:

    def __init__(self, db: Session):
        self.db = db

    def crear_obra(self, **kwargs) -> Obra:
        obra = Obra(**{k: v for k, v in kwargs.items() if hasattr(Obra, k)})
        self.db.add(obra)
        self.db.commit()
        self.db.refresh(obra)
        return obra

    def obtener_obra_por_id(self, obra_id: UUID) -> Optional[Obra]:
        return self.db.query(Obra).filter(Obra.id_obra == obra_id).first()

    def obtener_por_mal_id(self, mal_id: int) -> Optional[Obra]:
        return self.db.query(Obra).filter(Obra.mal_id == mal_id).first()

    def obtener_obra_por_nombre(self, nombre: str) -> Optional[Obra]:
        return self.db.query(Obra).filter(Obra.nombre == nombre).first()

    def obtener_todas_obras(self) -> List[Obra]:
        return self.db.query(Obra).all()

    def upsert_desde_jikan(self, datos: dict) -> Obra:
        """Inserta o actualiza una obra a partir de datos de Jikan."""
        mal_id = datos.get("mal_id")
        obra = self.obtener_por_mal_id(mal_id) if mal_id else None
        if obra:
            for k, v in datos.items():
                if hasattr(Obra, k):
                    setattr(obra, k, v)
        else:
            obra = Obra(**{k: v for k, v in datos.items() if hasattr(Obra, k)})
            self.db.add(obra)
        self.db.commit()
        self.db.refresh(obra)
        return obra

    def actualizar_obra(self, obra_id: UUID, datos_actualizar: dict) -> Optional[Obra]:
        obra = self.obtener_obra_por_id(obra_id)
        if not obra:
            return None
        for key, value in datos_actualizar.items():
            if hasattr(Obra, key):
                setattr(obra, key, value)
        self.db.commit()
        self.db.refresh(obra)
        return obra

    def eliminar_obra(self, obra_id: UUID) -> bool:
        obra = self.obtener_obra_por_id(obra_id)
        if not obra:
            return False
        self.db.delete(obra)
        self.db.commit()
        return True
