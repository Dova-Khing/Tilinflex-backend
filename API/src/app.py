"""
Archivo principal de la aplicación FastAPI. Aquí se inicializa la aplicación, se configuran los eventos de inicio y se registran los routers."""
from fastapi import FastAPI
from API.database.config import engine, Base

# Importar todos los modelos para que SQLAlchemy los reconozca
from API.src.entities import (
    Usuario, Suscripcion, Obra, Categoria,
    Perfil, Genero, DetalleSuscripcion, HistorialReproduccion
)

# Importar los routers
from API.endpoints import (
    usuarios, obras, categorias, generos,
    suscripcion, perfil, historial_reproduccion, detalle_suscripcion
)

app = FastAPI(title="Tilinflex API")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# Registrar routers
app.include_router(usuarios.router)
app.include_router(obras.router)
app.include_router(categorias.router)
app.include_router(generos.router)
app.include_router(suscripcion.router)
app.include_router(perfil.router)
app.include_router(historial_reproduccion.router)
app.include_router(detalle_suscripcion.router)
