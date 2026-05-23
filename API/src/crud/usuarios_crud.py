import re
import logging
from uuid import UUID
import pycountry
from sqlalchemy.orm import Session
from typing import List, Optional
from API.src.entities.usuarios import Usuario
from API.auth.security import PasswordManager

logger = logging.getLogger(__name__)

_PAISES_PERMITIDOS = {
    "AR", "BO", "BR", "CL", "CO", "CR", "CU", "EC", "SV", "GT",
    "GY", "HN", "NI", "PA", "PY", "PE", "DO", "SR", "UY", "VE", "US", "ES",
}


def _validar_email(email: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))


def _validar_pais(pais: str) -> bool:
    try:
        resultado = pycountry.countries.search_fuzzy(pais)
        return bool(resultado) and resultado[0].alpha_2 in _PAISES_PERMITIDOS
    except (AttributeError, LookupError):
        return False


def _validar_nombre(valor: str) -> bool:
    """Acepta letras con tildes, espacios, guiones y apóstrofes."""
    return bool(valor) and all(c.isalpha() or c in (" ", "-", "'") for c in valor)


class UsuarioCRUD:

    def __init__(self, db: Session):
        self.db = db

    def crear_usuario(
        self,
        nombre: str,
        apellido: str,
        email: str,
        contrasena: str,
        telefono: str = None,
        edad: int = None,
        pais: str = None,
        admin: bool = False,
    ) -> Optional[Usuario]:
        if not _validar_email(email):
            raise ValueError("El formato del email es inválido.")
        if pais and not _validar_pais(pais):
            raise ValueError("El país no es válido.")
        if edad is not None and edad < 18:
            raise ValueError("La edad debe ser mayor o igual a 18 años.")
        if not _validar_nombre(nombre) or not _validar_nombre(apellido):
            raise ValueError("Nombre o apellido inválido.")

        nuevo = Usuario(
            nombre=nombre.strip().capitalize(),
            apellido=apellido.strip().capitalize(),
            email=email.lower().strip(),
            telefono=telefono,
            contrasena_hash=PasswordManager.hash_password(contrasena),
            admin=admin,
            pais=pais,
            edad=edad,
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo

    def obtener_usuario(self, usuario_id: UUID) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.email == email.lower().strip()).first()

    def obtener_usuario_por_telefono(self, telefono: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.telefono == telefono.strip()).first()

    def obtener_todos_usuarios(self) -> List[Usuario]:
        return self.db.query(Usuario).all()

    def autenticar_usuario(self, email: str, contrasena: str) -> Optional[Usuario]:
        usuario = self.obtener_usuario_por_email(email)
        if not usuario or not usuario.activo:
            return None
        if PasswordManager.verify_password(contrasena, usuario.contrasena_hash):
            return usuario
        return None

    def cambiar_contrasena(self, usuario_id: UUID, contrasena_actual: str, nueva_contrasena: str) -> bool:
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return False

        if not PasswordManager.verify_password(contrasena_actual, usuario.contrasena_hash):
            raise ValueError("La contraseña actual es incorrecta.")

        es_valida, mensaje = PasswordManager.validate_password_strength(nueva_contrasena)
        if not es_valida:
            raise ValueError(f"Nueva contraseña inválida: {mensaje}")

        usuario.contrasena_hash = PasswordManager.hash_password(nueva_contrasena)
        self.db.commit()
        return True

    def actualizar_usuario(self, usuario_id: UUID, **kwargs) -> Optional[Usuario]:
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return None

        if "email" in kwargs:
            email = kwargs["email"]
            if not _validar_email(email):
                raise ValueError("Email inválido")
            existente = self.obtener_usuario_por_email(email)
            if existente and existente.id_usuario != usuario_id:
                raise ValueError("El email ya está registrado")
            kwargs["email"] = email.lower().strip()

        if "telefono" in kwargs and kwargs["telefono"]:
            kwargs["telefono"] = kwargs["telefono"].strip()

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or not nombre.strip():
                raise ValueError("El nombre es obligatorio")
            kwargs["nombre"] = nombre.strip().capitalize()

        if "apellido" in kwargs:
            apellido = kwargs["apellido"]
            if not apellido or not apellido.strip():
                raise ValueError("El apellido es obligatorio")
            kwargs["apellido"] = apellido.strip().capitalize()

        if "contrasena" in kwargs:
            contrasena = kwargs.pop("contrasena")
            es_valida, mensaje = PasswordManager.validate_password_strength(contrasena)
            if not es_valida:
                raise ValueError(f"Contraseña inválida: {mensaje}")
            kwargs["contrasena_hash"] = PasswordManager.hash_password(contrasena)

        for key, value in kwargs.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)

        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def eliminar_usuario(self, usuario_id: UUID) -> bool:
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return False
        self.db.delete(usuario)
        self.db.commit()
        return True

    def desactivar_usuario(self, usuario_id: UUID) -> Optional[Usuario]:
        return self.actualizar_usuario(usuario_id, activo=False)

    def obtener_usuarios_admin(self) -> List[Usuario]:
        return self.db.query(Usuario).filter(Usuario.admin == True).all()

    def es_admin(self, usuario_id: UUID) -> bool:
        usuario = self.obtener_usuario(usuario_id)
        return usuario.admin if usuario else False
