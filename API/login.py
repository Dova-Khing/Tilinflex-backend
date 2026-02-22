"""
Sistema de Gestión de una plataforma de streaming con ORM SQLAlchemy y Neon PostgreSQL
API REST con FastAPI - Sin interfaz de consola
"""

import uvicorn
#from apis import auth, usuario, historial_reproduccion, genero, suscripcion, perfil, categoria, obra
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sistema de Gestión de una plataforma de streaming",
    description="API REST para gestión de usuarios, contenido y suscripciones con autenticación",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
Incluir los Routers de las apis cuando este terminados

app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(historial_reproduccion.router)
app.include_router(genero.router)
app.include_router(suscripcion.router)
app.include_router(perfil.router)
app.include_router(categoria.router)
app.include_router(obra.router)

"""

@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    print("Iniciando Sistema de Gestión de una plataforma de streaming...")
    print("Configurando base de datos...")
    print("Sistema listo para usar.")
    print("Documentación disponible en: http://localhost:8000/docs")


@app.get("/", tags=["raíz"])
async def root():
    """Endpoint raíz que devuelve información básica de la API."""
    return {
        "mensaje": "Bienvenido al Sistema de Gestión de una plataforma de streaming",
        "version": "1.0.0",
        "documentacion": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "autenticacion": "/auth",
            "usuarios": "/usuarios",
            "historial_reproduccion": "/historial",
            "generos": "/generos",
            "suscripciones": "/suscripciones",
            "perfiles": "/perfiles",
            "categorias": "/categorias",
            "obras": "/obras",
        },
    }


def main():
    """Función principal para ejecutar el servidor"""
    print("Iniciando servidor FastAPI...")
    uvicorn.run(
        "login:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()