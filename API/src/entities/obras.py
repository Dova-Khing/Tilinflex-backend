from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID

from API.database.config import Base


class Obra(Base):
    __tablename__ = 'obras'

    __table_args__ = (
        UniqueConstraint('mal_id', name='uq_obras_mal_id'),
    )

    id_obra: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mal_id: int = Column(Integer, nullable=True)
    nombre: str = Column(String(200), nullable=False)
    nombre_japones: str = Column(String(200), nullable=True)
    descripcion: str = Column(Text, nullable=True)
    tipo: str = Column(String(20), nullable=True)       # TV, Movie, ONA, OVA
    episodios: int = Column(Integer, nullable=True)
    anio: int = Column(Integer, nullable=True)
    temporada: str = Column(String(20), nullable=True)  # spring, summer, fall, winter
    estado: str = Column(String(30), nullable=True)     # airing, complete, upcoming
    puntuacion: float = Column(Float, nullable=True)
    rango: int = Column(Integer, nullable=True)
    duracion: str = Column(String(50), nullable=True)
    estudios: str = Column(String(300), nullable=True)
    generos_externos: str = Column(Text, nullable=True)
    thumbnail_url: str = Column(Text, nullable=True)
    banner_url: str = Column(Text, nullable=True)
    trailer_url: str = Column(Text, nullable=True)
    fecha_registro: datetime = Column(DateTime, default=datetime.utcnow)
    id_categoria: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("categorias.id_categoria"), nullable=True)
    id_genero: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("generos.id_genero"), nullable=True)

    categoria = relationship("Categoria", back_populates="obras")
    generos = relationship("Genero", back_populates="obras")
    historial = relationship("HistorialReproduccion", back_populates="obra", cascade="all, delete")

    def __repr__(self) -> str:
        return f"<Obra(id_obra={self.id_obra}, nombre='{self.nombre}', mal_id={self.mal_id})>"

    def __to_dict__(self) -> dict:
        return {
            "id_obra":          str(self.id_obra),
            "mal_id":           self.mal_id,
            "nombre":           self.nombre,
            "nombre_japones":   self.nombre_japones,
            "descripcion":      self.descripcion,
            "tipo":             self.tipo,
            "episodios":        self.episodios,
            "anio":             self.anio,
            "temporada":        self.temporada,
            "estado":           self.estado,
            "puntuacion":       self.puntuacion,
            "rango":            self.rango,
            "duracion":         self.duracion,
            "estudios":         self.estudios,
            "generos_externos": self.generos_externos,
            "thumbnail_url":    self.thumbnail_url,
            "banner_url":       self.banner_url,
            "trailer_url":      self.trailer_url,
            "fecha_registro":   self.fecha_registro.isoformat(),
            "id_categoria":     str(self.id_categoria) if self.id_categoria else None,
            "id_genero":        str(self.id_genero) if self.id_genero else None,
        }
