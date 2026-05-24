"""
Tests de usuarios y autenticación.
Cubre: registro, login, protección de endpoints y seguridad.
"""

import pytest

USUARIO_BASE = {
    "nombre": "Juan",
    "apellido": "Perez",
    "email": "juan@test.com",
    "contrasena": "Clave123!",
}


# ── Test 1: Registro exitoso ────────────────────────────────────────────────

def test_registro_usuario(client):
    res = client.post("/usuarios/", json=USUARIO_BASE)
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == USUARIO_BASE["email"]
    assert data["nombre"] == USUARIO_BASE["nombre"]


# ── Test 2: No se puede registrar como admin ────────────────────────────────

def test_registro_no_otorga_admin(client):
    payload = {**USUARIO_BASE, "admin": True}
    res = client.post("/usuarios/", json=payload)
    assert res.status_code == 201
    # admin no aparece en la respuesta porque fue removido del schema
    data = res.json()
    assert data.get("admin") is None or data.get("admin") is False


# ── Test 3: Login exitoso devuelve token ────────────────────────────────────

def test_login_exitoso(client):
    client.post("/usuarios/", json=USUARIO_BASE)
    res = client.post("/auth/login", json={
        "email": USUARIO_BASE["email"],
        "contrasena": USUARIO_BASE["contrasena"],
    })
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"


# ── Test 4: Login con credenciales incorrectas devuelve 401 ─────────────────

def test_login_credenciales_incorrectas(client):
    client.post("/usuarios/", json=USUARIO_BASE)
    res = client.post("/auth/login", json={
        "email": USUARIO_BASE["email"],
        "contrasena": "contrasena_incorrecta",
    })
    assert res.status_code == 401


# ── Test 5: GET /es-admin requiere autenticación ────────────────────────────

def test_es_admin_requiere_auth(client):
    res_reg = client.post("/usuarios/", json=USUARIO_BASE)
    usuario_id = res_reg.json()["id_usuario"]
    res = client.get(f"/usuarios/{usuario_id}/es-admin")
    assert res.status_code == 401


# ── Test 6: GET /{id} requiere autenticación ────────────────────────────────

def test_obtener_usuario_requiere_auth(client):
    res_reg = client.post("/usuarios/", json=USUARIO_BASE)
    usuario_id = res_reg.json()["id_usuario"]
    res = client.get(f"/usuarios/{usuario_id}")
    assert res.status_code == 401
