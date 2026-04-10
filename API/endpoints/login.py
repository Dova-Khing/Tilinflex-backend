from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from API.src.core.auth import create_access_token
from API.src.core.config import get_settings
from API.src.core.responses import success_response
from API.database.config import get_db
from API.src.entities.usuarios import Usuario
from API.auth.security import PasswordManager


router = APIRouter(prefix="/auth", tags=["Autenticación"])


class LoginRequest(BaseModel):
    email: str
    contrasena: str


@router.post("/login")
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == datos.email).first()

    if not user or not PasswordManager.verify_password(datos.contrasena, user.contrasena_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )

    settings = get_settings()
    access_token = create_access_token(
        subject=user.id_usuario,
        email=user.email,
        admin=user.admin,
        settings=settings,
    )

    return success_response(
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes * 60,
            "admin": user.admin,
        },
        message="Login exitoso",
    )
