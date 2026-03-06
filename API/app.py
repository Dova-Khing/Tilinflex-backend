"""
Archivo principal de la aplicacion FastAPI.
Inicializa la aplicacion, configura los eventos de inicio y registra los routers.
"""

from fastapi import FastAPI
from API.database.config import engine, Base

# Importar todos los modelos antes del create_all para que SQLAlchemy los reconozca
from API.src.entities.usuarios import Usuario
from API.src.entities.suscripciones import Suscripcion
from API.src.entities.obras import Obra
from API.src.entities.categoria import Categoria
from API.src.entities.perfil import Perfil
from API.src.entities.generos import Genero
from API.src.entities.detalle_suscripcion import DetalleSuscripcion
from API.src.entities.historial_reproduccion import HistorialReproduccion

# Importar los routers
from API.endpoints import (
    usuario, obras, categorias, genero,
    suscripcion, perfil, historial_reproduccion, detalle_suscripcion
)

app = FastAPI(title="Tilinflex API")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(usuario.router)
app.include_router(obras.router)
app.include_router(categorias.router)
app.include_router(genero.router)
app.include_router(suscripcion.router)
app.include_router(perfil.router)
app.include_router(historial_reproduccion.router)
app.include_router(detalle_suscripcion.router)
