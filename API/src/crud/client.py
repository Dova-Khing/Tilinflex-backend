"""
Cliente HTTP para conectar con los endpoints de la API FastAPI.
Adaptado a la estructura de respuesta estándar: { "success", "data", "message" }.
En caso de error, la API devuelve { "success": false, "error": { "code", "message", "details" } }.
"""
import httpx

BASE_URL = "http://localhost:8000"

_auth_token: str | None = None


def set_auth_token(token: str | None) -> None:
    """Guarda el JWT para enviarlo como Authorization: Bearer en las peticiones siguientes."""
    global _auth_token
    _auth_token = token


def _auth_headers() -> dict[str, str]:
    if _auth_token:
        return {"Authorization": f"Bearer {_auth_token}"}
    return {}


def _unwrap(response_json: dict | list) -> dict | list:
    """Extrae el campo 'data' de la respuesta estándar de la API."""
    if isinstance(response_json, dict) and response_json.get("success") is True and "data" in response_json:
        return response_json["data"]
    return response_json


def _get(url: str, **kwargs) -> dict | list:
    headers = {**_auth_headers(), **kwargs.pop("headers", {})}
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        r = client.get(url, headers=headers, **kwargs)
        r.raise_for_status()
        return _unwrap(r.json())


def _post(url: str, json: dict, **kwargs) -> dict:
    headers = {**_auth_headers(), **kwargs.pop("headers", {})}
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        r = client.post(url, json=json, headers=headers, **kwargs)
        r.raise_for_status()
        if r.status_code == 204:
            return {}
        return _unwrap(r.json())


def _put(url: str, json: dict, **kwargs) -> dict:
    headers = {**_auth_headers(), **kwargs.pop("headers", {})}
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        r = client.put(url, json=json, headers=headers, **kwargs)
        r.raise_for_status()
        if r.status_code == 204:
            return {}
        return _unwrap(r.json())


def _delete(url: str, **kwargs) -> None:
    headers = {**_auth_headers(), **kwargs.pop("headers", {})}
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        r = client.delete(url, headers=headers, **kwargs)
        r.raise_for_status()