"""
Menú por consola que usa el CRUD (cliente de la API).
Al ejecutar main.py se inicia la API en segundo plano (uvicorn) y luego el menú.
"""
import sys
import threading
import time

# Permitir importar desde src cuando se ejecuta desde la raíz del proyecto
sys.path.insert(0, ".")

from API.src.crud import (
    usuarios_crud,
    suscripciones_crud,
    perfil_crud,
    obras_crud,
    historial_reproducciones,
    generos_crud,
    detalle_suscripcion_crud,
    categoria_crud
)

def mostrar_usuarios():
    try:
        usuarios = usuarios_crud.obtener_todos_usuarios()
        if not usuarios:
            print("  No hay usuarios.")
            return
        for u in usuarios:
            print(f"  {u['id']} | {u['nombre']} | {u['email']} | activo={u['activo']}")
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print("  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar.")
        else:
            print(f"  Error: {e}")


def mostrar_suscripciones():
    try:
        suscripciones = suscripciones_crud.obtener_todas_las_suscripciones()
        if not suscripciones:
            print("  No hay suscripciones.")
            return
        for p in suscripciones:
            print(f"  {p['id_suscripcion']} | {p['tipo_suscripcion']}")
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print("  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar.")
        else:
            print(f"  Error: {e}")

def mostrar_perfiles():
    try:
        perfiles = perfil_crud.obtener_todos()
        if not perfiles:
            print("  No hay perfiles.")
            return
        for p in perfiles:
            print(f"  {p['id_perfil']} | {p['nombre_perfil']} | ID usuario: {p['id_usuario']}")
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print("  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar.")
        else:
            print(f"  Error: {e}")

def mostrar_obras():
    try:
        obras = obras_crud.obtener_todas_las_obras()
        if not obras:
            print("  No hay obras.")
            return
        for o in obras:
            print(f"  {o['id_obra']} | {o['nombre']} | ID género: {o['id_genero']}")
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print("  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar.")
        else:
            print(f"  Error: {e}")

def mostrar_historial():
    try:
        historial = historial_reproducciones.obtener_todos()
        if not historial:
            print("  No hay reproducciones.")
            return
        for h in historial:
            print(f"  {h['id_historial_reproduccion']} | ID perfil: {h['id_perfil']} | Fecha: {h['fecha_reproduccion']}")
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print("  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar.")
        else:
            print(f"  Error: {e}")

def mostrar_generos():
    try:
        generos = generos_crud.obtener_todos_generos()
        if not generos:
            print("  No hay géneros.")
            return
        for g in generos:
            print(f"  {g['id_genero']} | {g['nombre_genero']}")
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print("  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar.")
        else:
            print(f"  Error: {e}")

def mostrar_detalle_suscripciones():
    try:
        detalles = detalle_suscripcion_crud.obtener_todos()
        if not detalles:
            print("  No hay detalles de suscripciones.")
            return
        for d in detalles:
            print(f"  ID detalle: {d['id_detalle']} | ID suscripción: {d['id_suscripcion']} | Valor: {d['valor']}")
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print("  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar.")
        else:
            print(f"  Error: {e}")

def mostrar_categorias():
    try:
        categorias = categoria_crud.obtener_todas_categorias()
        if not categorias:
            print("  No hay categorías.")
            return
        for c in categorias:
            print(f"  {c['id_categoria']} | {c['nombre_categoria']}")
    except Exception as e:
        err = str(e)
        if "10061" in err or "Connection refused" in err or "denegó" in err.lower():
            print("  No se pudo conectar a la API. Espera unos segundos y vuelve a intentar.")
        else:
            print(f"  Error: {e}")

def menu_usuarios():
    while True:
        print("\n--- Usuarios ---")
        print("1. Listar  2. Ver uno  3. Crear  4. Actualizar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            mostrar_usuarios()
        elif op == "2":
            uid = input("ID usuario: ").strip()
            if uid:
                try:
                    u = usuarios_crud.obtener_usuario(uid)
                    print(f"  {u}")
                except Exception as e:
                    print(f"  Error: {e}")
        elif op == "3":
            nombre = input("Nombre: ").strip()
            nombre_usuario = input("Nombre usuario: ").strip()
            email = input("Email: ").strip()
            contraseña = input("Contraseña: ").strip()
            if nombre and nombre_usuario and email and contraseña:
                try:
                    usuarios_crud.crear_usuario(nombre, nombre_usuario, email, contraseña)
                    print("  Usuario creado.")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("  Faltan datos.")
        elif op == "4":
            uid = input("ID usuario: ").strip()
            if not uid:
                continue
            nombre = input("Nombre (vacío=no cambiar): ").strip()
            email = input("Email (vacío=no cambiar): ").strip()
            try:
                kwargs = {}
                if nombre:
                    kwargs["nombre"] = nombre
                if email:
                    kwargs["email"] = email
                usuarios_crud.actualizar_usuario(uid, **kwargs)
                print("  Usuario actualizado.")
            except Exception as e:
                print(f"  Error: {e}")
        elif op == "5":
            uid = input("ID usuario a eliminar: ").strip()
            if uid:
                try:
                    usuarios_crud.eliminar_usuario(uid)
                    print("  Usuario eliminado.")
                except Exception as e:
                    print(f"  Error: {e}")

def menu_perfiles():
    while True:
        print("\n--- Perfiles ---")
        print("1. Listar  2. Ver uno  3. Crear  4. Actualizar  5. Eliminar  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            mostrar_perfiles()
        if op == "2":
            pid = input("ID perfil: ").strip()
            if pid:
                try:
                    p = perfil_crud.obtener_por_id(pid)
                    print(f"  {p}")
                except Exception as e:
                    print(f"  Error: {e}")
        if op == "3":
            nombre = input("Nombre perfil: ").strip()
            uid = input("ID usuario: ").strip()
            if nombre and uid:
                try:
                    perfil_crud.crear_perfil(nombre, uid)
                    print("  Perfil creado.")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("  Faltan datos.")
        if op == "4":
            pid = input("ID perfil: ").strip()
            if not pid:
                continue
            nombre = input("Nombre perfil (vacío=no cambiar): ").strip()
            try:
                kwargs = {}
                if nombre:
                    kwargs["nombre_perfil"] = nombre
                perfil_crud.actualizar_perfil(pid, **kwargs)
                print("  Perfil actualizado.")
            except Exception as e:
                print(f"  Error: {e}")
        if op == "5":
            pid = input("ID perfil a eliminar: ").strip()
            if pid:
                try:
                    perfil_crud.eliminar_perfil(pid)
                    print("  Perfil eliminado.")
                except Exception as e:
                    print(f"  Error: {e}")

def menu_suscripciones():
    while True:
        print("\n--- Suscripciones ---")
        print("1. Listar  2. Ver una  3. Crear  4. Actualizar 0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            mostrar_suscripciones()
        if op == "2":
            sid = input("ID suscripción: ").strip()
            if sid:
                try:
                    s = suscripciones_crud.obtener_por_id(sid)
                    print(f"  {s}")
                except Exception as e:
                    print(f"  Error: {e}")
        if op == "3":
            tipo = input("Tipo suscripción: ").strip()
            if tipo:
                try:
                    suscripciones_crud.crear_suscripcion(tipo)
                    print("  Suscripción creada.")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("  Faltan datos.")
        if op == "4":
            sid = input("ID suscripción: ").strip()
            if not sid:
                continue
            tipo = input("Tipo suscripción (vacío=no cambiar): ").strip()
            try:
                kwargs = {}
                if tipo:
                    kwargs["tipo_suscripcion"] = tipo
                suscripciones_crud.actualizar_suscripcion(sid, **kwargs)
                print("  Suscripción actualizada.")
            except Exception as e:
                print(f"  Error: {e}")

def menu_obras():
    while True:
        print("\n--- Obras ---")
        print("1. Listar  2. Ver una  3. Crear  4. Actualizar 5. Eliminar 0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            mostrar_obras()
        if op == "2":
            oid = input("ID obra: ").strip()
            if oid:
                try:
                    o = obras_crud.obtener_por_id(oid)
                    print(f"  {o}")
                except Exception as e:
                    print(f"  Error: {e}")
        if op == "3":
            nombre = input("Nombre obra: ").strip()
            gid = input("ID género: ").strip()
            if nombre and gid:
                try:
                    obras_crud.crear_obra(nombre, gid)
                    print("  Obra creada.")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("  Faltan datos.")
        if op == "4":
            oid = input("ID obra: ").strip()
            if not oid:
                continue
            nombre = input("Nombre obra (vacío=no cambiar): ").strip()
            gid = input("ID género (vacío=no cambiar): ").strip()
            try:
                kwargs = {}
                if nombre:
                    kwargs["nombre"] = nombre
                if gid:
                    kwargs["id_genero"] = gid
                obras_crud.actualizar_obra(oid, **kwargs)
                print("  Obra actualizada.")
            except Exception as e:
                print(f"  Error: {e}")
        if op == "5":
            oid = input("ID obra a eliminar: ").strip()
            if oid:
                try:
                    obras_crud.eliminar_obra(oid)
                    print("  Obra eliminada.")
                except Exception as e:
                    print(f"  Error: {e}")

def menu_historial():
    while True:
        print("\n--- Historial de reproducciones ---")
        print("1. Listar  2. Ver uno  3. Crear  4. Actualizar 0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            mostrar_historial()
        if op == "2":
            hid = input("ID historial: ").strip()
            if hid:
                try:
                    h = historial_reproducciones.obtener_por_id(hid)
                    print(f"  {h}")
                except Exception as e:
                    print(f"  Error: {e}")
        if op == "3":
            pid = input("ID perfil: ").strip()
            fecha = input("Fecha reproducción (YYYY-MM-DD): ").strip()
            if pid and fecha:
                try:
                    historial_reproducciones.crear_historial(pid, fecha)
                    print("  Historial creado.")
                except Exception as e:
                    print(f"  Error: {e}")
            else:
                print("  Faltan datos.")
        if op == "4":
            hid = input("ID historial: ").strip()
            if not hid:
                continue
            pid = input("ID perfil (vacío=no cambiar): ").strip()
            fecha = input("Fecha reproducción (YYYY-MM-DD, vacío=no cambiar): ").strip()
            try:
                kwargs = {}
                if pid:
                    kwargs["id_perfil"] = pid
                if fecha:
                    kwargs["fecha_reproduccion"] = fecha
                historial_reproducciones.actualizar_historial(hid, **kwargs)
                print("  Historial actualizado.")
            except Exception as e:
                print(f"  Error: {e}")

def menu_generos():
    while True:
        print("\n--- Géneros ---")
        print("1. Listar  2. Ver uno  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            mostrar_generos()
        if op == "2":
            gid = input("ID género: ").strip()
            if gid:
                try:
                    g = generos_crud.obtener_por_id(gid)
                    print(f"  {g}")
                except Exception as e:
                    print(f"  Error: {e}")

def menu_detalle():
    while True:
        print("\n--- Detalle de suscripciones ---")
        print("1. Listar  2. Ver uno  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            mostrar_detalle_suscripciones()
        if op == "2":
            did = input("ID detalle: ").strip()
            if did:
                try:
                    d = detalle_suscripcion_crud.obtener_por_id(did)
                    print(f"  {d}")
                except Exception as e:
                    print(f"  Error: {e}")

def menu_categorias():
    while True:
        print("\n--- Categorías ---")
        print("1. Listar  2. Ver una  0. Volver")
        op = input("Opción: ").strip()
        if op == "0":
            break
        if op == "1":
            mostrar_categorias()
        if op == "2":
            cid = input("ID categoría: ").strip()
            if cid:
                try:
                    c = categoria_crud.obtener_por_id(cid)
                    print(f"  {c}")
                except Exception as e:
                    print(f"  Error: {e}")


def _iniciar_api():
    """Ejecuta uvicorn en un hilo en segundo plano."""
    import uvicorn
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, log_level="warning")


def main():
    print("API Plataforma de Streaming - Menú por consola")
    print("Iniciando API en http://localhost:8000 ...")
    server = threading.Thread(target=_iniciar_api, daemon=True)
    #server.start()
    time.sleep(1.5)
    print("API lista.\n")
    while True:
        print("\n========== MENÚ ==========")
        print("1. Usuarios  2. Perfiles  3. Categorías  4. Obras  5. Historial  6. Generos  7. Suscripciones  8. Detalle suscripciones  0. Salir")
        op = input("Opción: ").strip()
        if op == "0":
            print("Hasta luego.")
            break
        if op == "1":
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