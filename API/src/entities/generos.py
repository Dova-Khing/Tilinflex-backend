"""
ENTIDAD GENERO
MODELO DE DATOS PARA LA ENTIDAD GENERO
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel

from API.database.config import Base


class Genero(Base):
    """
    Modelo de Genero que representa la tabla 'generos'
    """

    __tablename__ = "generos"

    id_genero: uuid.UUID = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    nombre_genero: str = Column(String(100), nullable=False, unique=True)

    # --------------------
    # RELACION
    # --------------------

    obras = relationship("Obra", back_populates="generos", cascade="all, delete")

    def __repr__(self) -> str:
        return (
            f"<Genero(id_genero={self.id_genero}, "
            f"nombre_genero='{self.nombre_genero}')>"
        )


class GeneroResponse(BaseModel):
    id_genero: uuid.UUID
    nombre_genero: str

    class Config:
        from_attributes = True
