"""
Script de verificación de base de datos para CI.
Crea el esquema completo y verifica que todas las tablas existan.
"""

import sys
from sqlalchemy import inspect

from API.database.config import engine, Base

# Importar todos los modelos para que SQLAlchemy los registre
from API.src.entities.usuarios import Usuario
from API.src.entities.suscripciones import Suscripcion
from API.src.entities.obras import Obra
from API.src.entities.categoria import Categoria
from API.src.entities.perfil import Perfil
from API.src.entities.generos import Genero
from API.src.entities.detalle_suscripcion import DetalleSuscripcion
from API.src.entities.historial_reproduccion import HistorialReproduccion

TABLAS_ESPERADAS = [
    "usuarios",
    "suscripciones",
    "obras",
    "categorias",
    "perfiles",
    "generos",
    "detalle_suscripcion",
    "historial_reproduccion",
]


def main():
    print("Creando esquema de base de datos...")
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    tablas_existentes = inspector.get_table_names()

    print(f"Tablas creadas: {tablas_existentes}")

    faltantes = [t for t in TABLAS_ESPERADAS if t not in tablas_existentes]
    if faltantes:
        print(f"ERROR: Faltan tablas: {faltantes}")
        sys.exit(1)

    print("Verificación exitosa: todas las tablas fueron creadas correctamente.")


if __name__ == "__main__":
    main()
