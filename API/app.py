"""
Archivo principal de la aplicacion FastAPI.
Inicializa la aplicacion, configura los eventos de inicio y registra los routers.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from API.database.config import engine, Base

from API.src.entities.usuarios import Usuario
from API.src.entities.suscripciones import Suscripcion
from API.src.entities.obras import Obra
from API.src.entities.categoria import Categoria
from API.src.entities.perfil import Perfil
from API.src.entities.generos import Genero
from API.src.entities.detalle_suscripcion import DetalleSuscripcion
from API.src.entities.historial_reproduccion import HistorialReproduccion

from API.src.core.config import get_settings
from API.src.core.exceptions import AppException
from API.src.core.error_handlers import (
    app_exception_handler,
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from API.src.core.responses import success_response

from API.endpoints import (
    usuario,
    obras,
    categorias,
    genero,
    suscripcion,
    perfil,
    historial_reproduccion,
    detalle_suscripcion,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Tilinflex API",
    description="API con FastAPI, SQLAlchemy y PostgreSQL.",
    lifespan=lifespan,
)

_settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=_settings.cors_origins_list(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(usuario.router)
app.include_router(obras.router)
app.include_router(categorias.router)
app.include_router(genero.router)
app.include_router(suscripcion.router)
app.include_router(perfil.router)
app.include_router(historial_reproduccion.router)
app.include_router(detalle_suscripcion.router)


@app.get("/")
def inicio():
    return success_response(
        data={"mensaje": "Tilinflex API", "docs": "/docs"},
        message="Bienvenido a la API Tilinflex",
    )
