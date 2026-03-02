"""
API de Autenticación - Endpoints para gestión de la seguridad

TOCA MODIFICARLO, NO ADECUADO PARA EL PROYECTO.
"""

from uuid import UUID
from datetime import timedelta
from ..src.crud.usuarios_crud import UsuarioCRUD
from database.config import get_db
from ..src.entities.usuarios import Usuario
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import RespuestaAPI, UsuarioLogin, UsuarioResponse, UsuarioCreate
from sqlalchemy.orm import Session
from auth.security import TokenManager

router = APIRouter(prefix="/auth", tags=["autenticación"])


from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: dict


@router.post("/login", response_model=TokenResponse)
async def login(login_data: UsuarioLogin, db: Session = Depends(get_db)):
    try:
        print(f"Intento de login recibido:")
        print(f"Nombre usuario: {login_data.nombre_usuario}")
        print(f"Contraseña length: {len(login_data.contrasena)}")

        if not login_data.nombre_usuario or not login_data.contrasena:
            print("Campos vacíos")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario/email y la contraseña son obligatorios",
            )

        if len(login_data.contrasena) < 8:
            print("Contraseña muy corta")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña debe tener al menos 8 caracteres",
            )

        usuario_crud = UsuarioCRUD(db)
        print("Llamando a autenticar_usuario...")

        usuario = usuario_crud.autenticar_usuario(
            login_data.nombre_usuario, login_data.contrasena
        )

        if not usuario:
            print(
                "autenticar_usuario retornó None - credenciales incorrectas o usuario inactivo"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas o usuario inactivo",
            )

        access_token_expires = timedelta(minutes=60 * 24)
        access_token = TokenManager.create_access_token(
            data={
                "sub": usuario.nombre_usuario,
                "user_id": str(usuario.id),
                "email": usuario.email,
                "es_admin": usuario.es_admin,
                "nombre": usuario.nombre,
            },
            expires_delta=access_token_expires,
        )

        print(f"Login exitoso para: {usuario.nombre}")
        print(f"Token JWT generado exitosamente")

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=60 * 24 * 60,
            user={
                "id": str(usuario.id),
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "email": usuario.email,
                "es_admin": usuario.es_admin,
                "edad": usuario.edad,
                "pais": usuario.pais,
            },
        )

    except HTTPException:
        print("HTTPException en login")
        raise
    except Exception as e:
        print(f"ERROR inesperado en login: {str(e)}")
        print(f"Tipo de error: {type(e)}")
        import traceback

        print(f"Traceback: {traceback.format_exc()}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el login: {str(e)}",
        )


@router.post("/registro", response_model=UsuarioResponse)
async def registrar_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Registrar un nuevo usuario en el sistema
    """
    try:
        print(f"Registro de usuario recibido:")
        print(f"Nombre: {usuario_data.nombre}")
        print(f"Usuario: {usuario_data.nombre_usuario}")
        print(f"Email: {usuario_data.email}")

        usuario_crud = UsuarioCRUD(db)

        usuario = usuario_crud.crear_usuario(
            nombre=usuario_data.nombre,
            apellido=usuario_data.apellido,
            email=usuario_data.email,
            contrasena=usuario_data.contrasena,
            telefono=usuario_data.telefono,
            edad=usuario_data.edad,
            pais=usuario_data.pais,
            es_admin=False,
        )

        print(f"Usuario registrado exitosamente: {usuario.nombre}")
        return usuario

    except ValueError as e:
        print(f"Error de validación en registro: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"ERROR inesperado en registro: {str(e)}")
        import traceback

        print(f"Traceback: {traceback.format_exc()}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar usuario: {str(e)}",
        )


@router.post("/registro", response_model=UsuarioResponse)
async def registrar_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Registrar un nuevo usuario en el sistema
    """
    try:
        print(f"Registro de usuario recibido:")
        print(f"Nombre: {usuario_data.nombre}")
        print(f"Email: {usuario_data.email}")

        usuario_crud = UsuarioCRUD(db)

        # Crear el usuario (el CRUD ya tiene todas las validaciones)
        usuario = usuario_crud.crear_usuario(
            nombre=usuario_data.nombre,
            apellido=usuario_data.apellido,
            email=usuario_data.email,
            contrasena=usuario_data.contrasena,
            telefono=usuario_data.telefono,
            edad=usuario_data.edad,
            pais=usuario_data.pais,
            es_admin=False,  # Por defecto no es admin
        )

        print(f"Usuario registrado exitosamente: {usuario.nombre}")
        return usuario

    except ValueError as e:
        print(f"Error de validación en registro: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"ERROR inesperado en registro: {str(e)}")
        import traceback

        print(f"Traceback: {traceback.format_exc()}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar usuario: {str(e)}",
        )


@router.post("/crear-admin", response_model=RespuestaAPI)
async def crear_usuario_admin(db: Session = Depends(get_db)):
    try:
        usuario_crud = UsuarioCRUD(db)

        admin_existente = usuario_crud.obtener_admin_por_defecto()
        if admin_existente:
            return RespuestaAPI(
                mensaje="Ya existe un usuario administrador por defecto",
                exito=True,
                datos={"admin_id": str(admin_existente.id)},
            )

        from auth.security import PasswordManager

        contrasena_admin = PasswordManager.generate_secure_password(12)

        admin = usuario_crud.crear_usuario(
            nombre="Administrador del Sistema",
            apellido="",
            email="admin@system.com",
            contrasena=contrasena_admin,
            edad="99",
            pais="N/A",
            es_admin=True,
        )

        return RespuestaAPI(
            mensaje="Usuario administrador creado exitosamente",
            exito=True,
            datos={
                "admin_id": str(admin.id),
                "contrasena_temporal": contrasena_admin,
                "mensaje": "IMPORTANTE: Cambie esta contraseña en su primer inicio de sesión",
            },
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear administrador: {str(e)}",
        )


@router.get("/verificar/{usuario_id}", response_model=RespuestaAPI)
async def verificar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.obtener_usuario(usuario_id)

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        return RespuestaAPI(
            mensaje="Usuario verificado exitosamente",
            exito=True,
            datos={
                "usuario_id": str(usuario.id),
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "email": usuario.email,
                "edad": usuario.edad,
                "pais": usuario.pais,
                "activo": usuario.activo,
                "es_admin": usuario.es_admin,
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar usuario: {str(e)}",
        )


@router.get("/estado", response_model=RespuestaAPI)
async def estado_autenticacion():
    return RespuestaAPI(
        mensaje="Sistema de autenticación funcionando correctamente",
        exito=True,
        datos={
            "sistema": "Sistema de gestión de una plataforma de streaming ",
            "version": "1.0.0",
            "autenticacion": "Activa",
        },
    )


@router.get("/debug-usuarios")
async def debug_usuarios(db: Session = Depends(get_db)):
    """Endpoint temporal para debuggear usuarios"""
    usuarios = db.query(Usuario).all()
    return {
        "total_usuarios": len(usuarios),
        "usuarios": [
            {
                "id": str(u.id),
                "nombre": u.nombre,
                "apellido": u.apellido,
                "email": u.email,
                "pais": u.pais,
                "activo": u.activo,
                "es_admin": u.es_admin,
            }
            for u in usuarios
        ],
    }