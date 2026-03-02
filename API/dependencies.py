"""
Modulo de dependencias para FastAPI.
Contiene funciones de dependencia para autenticación y autorización.
"""



from fastapi import Depends, HTTPException, status
from API.auth import get_current_user

def require_admin(current_user = Depends(get_current_user)):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    return current_user
