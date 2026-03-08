"""
Menú por consola que usa el CRUD (cliente de la API).
Al ejecutar main.py se inicia la API en segundo plano (uvicorn) y luego el menú.
"""

import sys

from pycountry import db

sys.path.insert(0, ".")

from API.database import CATEGORIAS_DEFAULT, GENEROS_DEFAULT
from API.database.config import SessionLocal
from API.src.crud.usuarios_crud import UsuarioCRUD
from API.src.crud.suscripciones_crud import SuscripcionCRUD
from API.src.crud.perfil_crud import PerfilCRUD
from API.src.crud.obras_crud import ObraCRUD
from API.src.crud.historial_reproducciones import HistorialReproduccionCRUD
from API.src.crud.generos_crud import GeneroCRUD
from API.src.crud.detalle_suscripcion_crud import DetalleSuscripcionCRUD
from API.src.crud.categoria_crud import CategoriaCRUD
import os


def get_db():
    return SessionLocal()


# ─────────────────────────────────────────────
# MOSTRAR
# ─────────────────────────────────────────────


def mostrar_usuarios():
    db = get_db()
    try:
        usuarios = UsuarioCRUD(db).obtener_todos_usuarios()
        if not usuarios:
            print("  No hay usuarios.")
            return
        for u in usuarios:
            print(
                f"  {u.id_usuario} | {u.nombre} {u.apellido} | {u.email} | activo={u.activo}"
            )
    except Exception as e:
        print(f"  Error: {e}")
    finally:
        db.close()


def mostrar_suscripciones():
    db = get_db()
    try:
        suscripciones = SuscripcionCRUD(db).obtener_todas_las_suscripciones()
        if not suscripciones:
            print("  No hay suscripciones.")
            return
        for s in suscripciones:
            print(f"  {s.id_suscripcion} | {s.tipo_suscripcion}")
    except Exception as e:
        print(f"  Error: {e}")
    finally:
        db.close()


def mostrar_perfiles():
    db = get_db()
    try:
        perfiles = PerfilCRUD(db).obtener_todos()
        if not perfiles:
            print("  No hay perfiles.")
            return
        for p in perfiles:
            print(f"  {p.id_perfil} | {p.nombre_usuario} | ID usuario: {p.id_usuario}")
    except Exception as e:
        print(f"  Error: {e}")
    finally:
        db.close()


def mostrar_obras():
    db = get_db()
    try:
        obras = ObraCRUD(db).obtener_todas_las_obras()
        if not obras:
            print("  No hay obras.")
            return
        for o in obras:
            print(f"  {o.id_obra} | {o.nombre} | ID género: {o.id_genero}")
    except Exception as e:
        print(f"  Error: {e}")
    finally:
        db.close()


def mostrar_historial():
    db = get_db()
    try:
        historial = HistorialReproduccionCRUD(db).obtener_todos()
        if not historial:
            print("  No hay reproducciones.")
            return
        for h in historial:
            print(
                f"  {h.id_historial} | ID perfil: {h.id_perfil} | Fecha: {h.fecha_visualizacion}"
            )
    except Exception as e:
        print(f"  Error: {e}")
    finally:
        db.close()


def mostrar_generos():
    db = get_db()
    try:
        crud = GeneroCRUD(db)
        for nombre in GENEROS_DEFAULT:
            if not crud.obtener_genero_por_nombre(nombre):
                crud.crear_genero(nombre)
        generos = crud.obtener_todos_generos()
        if not generos:
            print("  No hay géneros.")
            return
        for g in generos:
            print(f"  {g.id_genero} | {g.nombre_genero}")
    except Exception as e:
        print(f"  Error: {e}")
    finally:
        db.close()


def mostrar_detalle_suscripciones():
    db = get_db()
    try:
        detalles = DetalleSuscripcionCRUD(db).obtener_todos()
        if not detalles:
            print("  No hay detalles de suscripciones.")
            return
        for d in detalles:
            print(
                f"  {d.id_detalle_suscripcion} | ID suscripción: {d.id_suscripcion} | Valor: {d.valor}"
            )
    except Exception as e:
        print(f"  Error: {e}")
    finally:
        db.close()


def mostrar_categorias():
    db = get_db()
    try:
        crud = CategoriaCRUD(db)
        for nombre in CATEGORIAS_DEFAULT:
            if not crud.obtener_categoria_por_nombre(nombre):
                crud.crear_categoria(nombre)
        categorias = crud.obtener_todas_categorias()
        if not categorias:
            print("  No hay categorías.")
            return
        for c in categorias:
            print(f"  {c.id_categoria} | {c.nombre_categoria}")
    except Exception as e:
        print(f"  Error: {e}")
    finally:
        db.close()


# ─────────────────────────────────────────────
# MENÚS
# ─────────────────────────────────────────────

def menu_usuarios():
    while True:
        print("\n--- Usuarios ---")
        print(
            "1. Listar \n"
            "2. Ver uno  \n"
            "3. Crear  \n"
            "4. Actualizar  \n"
            "5. Eliminar  \n"
            "0. Volver"
        )
        op = input("Opción: ").strip()
        if op == "0":
            break
        db = get_db()
        try:
            crud = UsuarioCRUD(db)
            if op == "1":
                mostrar_usuarios()

            elif op == "2":
                uid = input("ID usuario: ").strip()
                if uid:
                    u = crud.obtener_usuario(uid)
                    print(f"  {u}")

            elif op == "3":
                nombre = input("Nombre: ").strip()
                apellido = input("Apellido: ").strip()
                email = input("Email: ").strip()
                contrasena = input("Contraseña: ").strip()
                telefono = input("Teléfono (vacío=ninguno): ").strip() or None
                edad = input("Edad: ").strip()
                pais = input("País: ").strip()
                if nombre and apellido and email and contrasena:
                    crud.crear_usuario(
                        nombre=nombre,
                        apellido=apellido,
                        email=email,
                        contrasena=contrasena,
                        telefono=telefono,
                        edad=int(edad) if edad else None,
                        pais=pais or None,
                    )
                    print("  Usuario creado.")
                else:
                    print("  Faltan datos.")

            elif op == "4":
                uid = input("ID usuario: ").strip()
                if not uid:
                    continue
                nombre = input("Nombre (vacío=no cambiar): ").strip()
                email = input("Email (vacío=no cambiar): ").strip()
                kwargs = {}
                if nombre:
                    kwargs["nombre"] = nombre
                if email:
                    kwargs["email"] = email
                crud.actualizar_usuario(uid, **kwargs)
                print("  Usuario actualizado.")
            elif op == "5":
                uid = input("ID usuario a eliminar: ").strip()
                if uid:
                    crud.eliminar_usuario(uid)
                    print("  Usuario eliminado.")
        except Exception as e:
            print(f"  Error: {e}")
        finally:
            db.close()
        input("\n  Presioná Enter para continuar...")


def menu_perfiles():
    while True:
        print("\n--- Perfiles ---")
        print(
            "1. Listar \n"
            "2. Ver uno  \n"
            "3. Crear  \n"
            "4. Actualizar  \n"
            "5. Eliminar  \n"
            "0. Volver"
        )
        op = input("Opción: ").strip()
        if op == "0":
            break
        db = get_db()
        try:
            crud = PerfilCRUD(db)
            if op == "1":
                mostrar_perfiles()

            elif op == "2":
                pid = input("ID perfil: ").strip()

                if pid:
                    print(f"  {crud.obtener_por_id(pid)}")

            elif op == "3":
<<<<<<< Updated upstream
=======
                print(
                    "  Para crear un perfil, necesitás el ID de un usuario existente. \n Aquí esta la lista de usuarios:"
                )
                usuarios = crud.obtener_todos_usuarios()
                for u in usuarios:
                    print(f"    {u.id_usuario}: {u.nombre} {u.apellido}")
>>>>>>> Stashed changes
                nombre = input("Nombre perfil: ").strip()
                uid = input("ID usuario: ").strip()
                idioma = input("Idioma (vacío=es): ").strip() or "es"
                infantil = input("¿Es infantil? (s/n): ").strip().lower() == "s"
                if nombre and uid:
                    crud.crear_perfil(
                        nombre_usuario=nombre,
                        id_usuario=uid,
                        idioma=idioma,
                        es_infantil=infantil,
                    )
                    print("  Perfil creado.")
                else:
                    print("  Faltan datos.")

            elif op == "4":
                print("  actualizar un perfil, necesitás su ID. \n Aquí esta la lista de perfiles:")

                perfiles = crud.obtener_todos()
                for p in perfiles:
                    print(f"    {p.id_perfil}: {p.nombre_usuario}")
                pid = input("ID perfil: ").strip()
                if not pid:
                    continue
                nombre = input("Nombre perfil (vacío=no cambiar): ").strip()
                if nombre:
                    crud.actualizar_perfil(pid, nombre)
                    print("  Perfil actualizado.")
                else:
                    print("  No hubo cambios.")

            elif op == "5":
                print("  Para eliminar un perfil, necesitás su ID. \n Aquí esta la lista de perfiles:")
                perfiles = crud.obtener_todos()
                for p in perfiles:
                    print(f"    {p.id_perfil}: {p.nombre_usuario}")
                pid = input("ID perfil a eliminar: ").strip()
                if pid:
                    crud.eliminar_perfil(pid)
                    print("  Perfil eliminado.")
        except Exception as e:
            print(f"  Error: {e}")
        finally:
            db.close()
        input("\n  Presioná Enter para continuar...")


def menu_suscripciones():
    while True:
        print("\n--- Suscripciones ---")
        print(
            "1. Listar \n"
            "2. Ver una  \n"
            "3. Crear  \n"
            "4. Actualizar  \n"
            "0. Volver"
        )
        op = input("Opción: ").strip()
        if op == "0":
            break
        db = get_db()
        try:
            crud = SuscripcionCRUD(db)
            if op == "1":
                mostrar_suscripciones()
            elif op == "2":
                sid = input("ID suscripción: ").strip()
                if sid:
                    print(f"  {crud.obtener_suscripcion(sid)}")

            elif op == "3":
                from API.src.entities.suscripciones import SuscripcionBase
                tipo = input("Tipo (mensual/anual/trimestral): ").strip()
                print(
                    "  Para crear un perfil, necesitás el ID de un usuario existente. \n Aquí esta la lista de usuarios:"
                )
                usuarios = UsuarioCRUD(db).obtener_todos_usuarios()
                for u in usuarios:
                    print(f"    {u.id_usuario} -> {u.nombre} {u.apellido}")

                uid = input("ID usuario: ").strip()
                valor = input("Valor a pagar: ").strip()
                metodo = input("Método de pago (tarjeta_credito/tarjeta_debito/paypal/transferencia): ").strip()
                if tipo and uid and valor and metodo:
                    nueva_suscripcion = crud.crear_suscripcion(
                        SuscripcionBase(tipo_suscripcion=tipo, id_usuario=uid)
                    )
                    DetalleSuscripcionCRUD(db).crear_detalle_suscripcion(
                        valor=float(valor),
                        metodo_pago=metodo,
                        id_suscripcion=nueva_suscripcion.id_suscripcion
                    )
                    print("  Suscripción y pago registrados.")
                else:
                    print("  Faltan datos.")

            elif op == "4":
                sid = input("ID suscripción: ").strip()
                if not sid:
                    continue
                from API.src.entities.suscripciones import SuscripcionBase
                tipo = input("Tipo suscripción (vacío=no cambiar): ").strip()
                if tipo:
                    crud.actualizar_suscripcion(
                        sid, SuscripcionBase(tipo_suscripcion=tipo, id_usuario="00000000-0000-0000-0000-000000000000")
                    )
                    print("  Suscripción actualizada.")
        except Exception as e:
            print(f"  Error: {e}")
        finally:
            db.close()
        input("\n  Presioná Enter para continuar...")


def menu_obras():
    while True:
        print("\n--- Obras ---")
        print(
            "1. Listar \n"
            "2. Ver una  \n"
            "3. Crear  \n"
            "4. Actualizar \n"
            "5. Eliminar \n"
            "0. Volver"
        )
        op = input("Opción: ").strip()
        if op == "0":
            break
        db = get_db()
        try:
            crud = ObraCRUD(db)
            if op == "1":
                mostrar_obras()
            elif op == "2":
                oid = input("ID obra: ").strip()
                if oid:
                    print(f"  {crud.obtener_por_id(oid)}")
            elif op == "3":
                nombre = input("Nombre obra: ").strip()
                id_categoria = input("ID categoría: ").strip()
                id_genero = input("ID género: ").strip()
                anio = input("Año: ").strip()
                episodios = input("Episodios: ").strip()
                if nombre and id_categoria and id_genero and anio:
                    crud.crear_obra(
                        nombre=nombre,
                        id_categoria=id_categoria,
                        id_genero=id_genero,
                        anio=int(anio),
                        episodios=int(episodios) if episodios else 1,
                    )
                    print("  Obra creada.")
                else:
                    print("  Faltan datos.")
            elif op == "4":
                oid = input("ID obra: ").strip()
                if not oid:
                    continue
                nombre = input("Nombre obra (vacío=no cambiar): ").strip()
                gid = input("ID género (vacío=no cambiar): ").strip()
                kwargs = {}
                if nombre:
                    kwargs["nombre"] = nombre
                if gid:
                    kwargs["id_genero"] = gid
                crud.actualizar_obra(oid, **kwargs)
                print("  Obra actualizada.")
            elif op == "5":
                oid = input("ID obra a eliminar: ").strip()
                if oid:
                    crud.eliminar_obra(oid)
                    print("  Obra eliminada.")
        except Exception as e:
            print(f"  Error: {e}")
        finally:
            db.close()
        input("\n  Presioná Enter para continuar...")


def menu_historial():
    while True:
        print("\n--- Historial de reproducciones ---")
        print(
            "1. Listar \n"
            "2. Ver uno  \n"
            "0. Volver"
        )
        op = input("Opción: ").strip()
        if op == "0":
            break
        db = get_db()
        try:
            crud = HistorialReproduccionCRUD(db)
            if op == "1":
                mostrar_historial()
            elif op == "2":
                hid = input("ID historial: ").strip()
                if hid:
                    print(f"  {crud.obtener_por_id(hid)}")
        except Exception as e:
            print(f"  Error: {e}")
        finally:
            db.close()
        input("\n  Presioná Enter para continuar...")


def menu_generos():
    while True:
        print("\n--- Géneros ---")
        print(
            "1. Listar \n"
            "2. Ver uno  \n"
            "0. Volver"
        )
        op = input("Opción: ").strip()
        if op == "0":
            break
        db = get_db()
        try:
            crud = GeneroCRUD(db)
            if op == "1":
                mostrar_generos()
            elif op == "2":
                gid = input("ID género: ").strip()
                if gid:
                    print(f"  {crud.obtener_genero_por_id(gid)}")
        except Exception as e:
            print(f"  Error: {e}")
        finally:
            db.close()
        input("\n  Presioná Enter para continuar...")


def menu_detalle():
    while True:
        print("\n--- Detalle de suscripciones ---")
        print(
            "1. Listar \n"
            "2. Ver uno  \n"
            "0. Volver"
        )
        op = input("Opción: ").strip()
        if op == "0":
            break
        db = get_db()
        try:
            crud = DetalleSuscripcionCRUD(db)
            if op == "1":
                mostrar_detalle_suscripciones()
            elif op == "2":
                did = input("ID detalle: ").strip()
                if did:
                    print(f"  {crud.obtener_por_id(did)}")
        except Exception as e:
            print(f"  Error: {e}")
        finally:
            db.close()
        input("\n  Presioná Enter para continuar...")


def menu_categorias():
    while True:
        print("\n--- Categorías ---")
        print(
            "1. Listar \n"
            "2. Ver una  \n"
            "0. Volver"
        )
        op = input("Opción: ").strip()
        if op == "0":
            break
        db = get_db()
        try:
            crud = CategoriaCRUD(db)
            if op == "1":
                mostrar_categorias()
            elif op == "2":
                cid = input("ID categoría: ").strip()
                if cid:
                    print(f"  {crud.obtener_categoria_por_id(cid)}")
        except Exception as e:
            print(f"  Error: {e}")
        finally:
            db.close()
        input("\n  Presioná Enter para continuar...")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────


def main():
    print("API Plataforma de Streaming - Menú por consola")
    while True:
        print("\n========== MENÚ ==========")
        print(
            "1. Usuarios  \n"
            "2. Perfiles  \n"
            "3. Categorías  \n"
            "4. Obras  \n"
            "5. Historial  \n"
            "6. Géneros  \n"
            "7. Suscripciones  \n"
            "8. Detalle suscripciones  \n"
            "0. Salir"
        )
        op = input("Opción: ").strip()
        if op == "0":
            print("Hasta luego.")
            break
        elif op == "1":
            menu_usuarios()
        elif op == "2":
            menu_perfiles()
        elif op == "3":
            menu_categorias()
        elif op == "4":
            menu_obras()
        elif op == "5":
            menu_historial()
        elif op == "6":
            menu_generos()
        elif op == "7":
            menu_suscripciones()
        elif op == "8":
            menu_detalle()
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
