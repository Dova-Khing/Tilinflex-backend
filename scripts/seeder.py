"""
Seeder: inserta datos iniciales en la base de datos de forma idempotente.
Se puede ejecutar múltiples veces sin duplicar registros.
"""

import sys
from API.database.config import engine, SessionLocal, Base

from API.src.entities.usuarios import Usuario
from API.src.entities.categoria import Categoria
from API.src.entities.generos import Genero
from API.src.entities.obras import Obra
from API.auth.security import PasswordManager


# ---------------------------------------------------------------------------
# Datos de catálogos
# ---------------------------------------------------------------------------

CATEGORIAS = ["Película", "Serie", "Documental", "Anime"]

GENEROS = [
    "Acción", "Drama", "Comedia", "Terror", "Ciencia ficción",
    "Aventura", "Romance", "Suspenso(Thriller)", "Fantasía",
    "Musical", "Documental",
]

OBRAS_DUMMY = [
    {"nombre": "Breaking Bad",       "descripcion": "Un profesor de química se convierte en narcotraficante.", "episodios": 62,  "anio": 2008, "categoria": "Serie",       "genero": "Drama"},
    {"nombre": "Inception",          "descripcion": "Un ladrón que roba secretos a través de los sueños.",    "episodios": 1,   "anio": 2010, "categoria": "Película",     "genero": "Ciencia ficción"},
    {"nombre": "Attack on Titan",    "descripcion": "La humanidad lucha por sobrevivir contra gigantes.",     "episodios": 87,  "anio": 2013, "categoria": "Anime",        "genero": "Acción"},
    {"nombre": "Planet Earth II",    "descripcion": "Documental sobre la vida salvaje en distintos biomas.",  "episodios": 6,   "anio": 2016, "categoria": "Documental",   "genero": "Documental"},
    {"nombre": "The Office",         "descripcion": "La vida cotidiana de una oficina filmada como mockumentary.", "episodios": 201, "anio": 2005, "categoria": "Serie",  "genero": "Comedia"},
]

USUARIO_ADMIN = {
    "nombre": "Admin",
    "apellido": "Sistema",
    "email": "admin@tilinflex.com",
    "contrasena": "Admin123!",
    "edad": 30,
    "pais": "Colombia",
    "admin": True,
}

USUARIO_DEMO = {
    "nombre": "Usuario",
    "apellido": "Demo",
    "email": "demo@tilinflex.com",
    "contrasena": "Demo1234!",
    "edad": 25,
    "pais": "Colombia",
    "admin": False,
}


# ---------------------------------------------------------------------------
# Funciones de seed (idempotentes)
# ---------------------------------------------------------------------------

def seed_categorias(db):
    nuevas = 0
    for nombre in CATEGORIAS:
        existe = db.query(Categoria).filter(Categoria.nombre_categoria == nombre).first()
        if not existe:
            db.add(Categoria(nombre_categoria=nombre))
            nuevas += 1
    db.commit()
    print(f"  Categorías: {nuevas} insertadas, {len(CATEGORIAS) - nuevas} ya existían.")


def seed_generos(db):
    nuevos = 0
    for nombre in GENEROS:
        existe = db.query(Genero).filter(Genero.nombre_genero == nombre).first()
        if not existe:
            db.add(Genero(nombre_genero=nombre))
            nuevos += 1
    db.commit()
    print(f"  Géneros: {nuevos} insertados, {len(GENEROS) - nuevos} ya existían.")


def seed_usuarios(db):
    nuevos = 0
    for datos in [USUARIO_ADMIN, USUARIO_DEMO]:
        existe = db.query(Usuario).filter(Usuario.email == datos["email"]).first()
        if not existe:
            db.add(Usuario(
                nombre=datos["nombre"],
                apellido=datos["apellido"],
                email=datos["email"],
                contrasena_hash=PasswordManager.hash_password(datos["contrasena"]),
                edad=datos["edad"],
                pais=datos["pais"],
                admin=datos["admin"],
                activo=True,
            ))
            nuevos += 1
    db.commit()
    print(f"  Usuarios: {nuevos} insertados, {2 - nuevos} ya existían.")


def seed_obras(db):
    nuevas = 0
    for datos in OBRAS_DUMMY:
        existe = db.query(Obra).filter(Obra.nombre == datos["nombre"]).first()
        if existe:
            continue

        categoria = db.query(Categoria).filter(Categoria.nombre_categoria == datos["categoria"]).first()
        genero = db.query(Genero).filter(Genero.nombre_genero == datos["genero"]).first()

        if not categoria or not genero:
            print(f"  ADVERTENCIA: Categoría o género no encontrado para '{datos['nombre']}', omitiendo.")
            continue

        db.add(Obra(
            nombre=datos["nombre"],
            descripcion=datos["descripcion"],
            episodios=datos["episodios"],
            anio=datos["anio"],
            id_categoria=categoria.id_categoria,
            id_genero=genero.id_genero,
        ))
        nuevas += 1
    db.commit()
    print(f"  Obras: {nuevas} insertadas, {len(OBRAS_DUMMY) - nuevas} ya existían.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Iniciando seeder...")

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_categorias(db)
        seed_generos(db)
        seed_usuarios(db)
        seed_obras(db)
        print("Seeder completado exitosamente.")
    except Exception as e:
        db.rollback()
        print(f"ERROR en seeder: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
