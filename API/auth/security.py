"""
Módulo de seguridad para manejo de contraseñas
"""

from passlib.context import CryptContext
from typing import Tuple
import secrets
import string

# Configuración del contexto de hash
pwd_context = CryptContext(
    schemes=["bcrypt"],  # puedes cambiar a argon2 si quieres más seguridad
    deprecated="auto",
)


class PasswordManager:
    """Gestor de contraseñas con hash seguro usando passlib"""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Generar hash seguro de una contraseña
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verificar si una contraseña coincide con su hash
        """
        return pwd_context.verify(password, password_hash)

    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, str]:
        """
        Validar la fortaleza de una contraseña
        """
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"

        if len(password) > 128:
            return False, "La contraseña no puede exceder 128 caracteres"

        if not any(c.isupper() for c in password):
            return False, "La contraseña debe contener al menos una letra mayúscula"

        if not any(c.islower() for c in password):
            return False, "La contraseña debe contener al menos una letra minúscula"

        if not any(c.isdigit() for c in password):
            return False, "La contraseña debe contener al menos un número"

        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False, "La contraseña debe contener al menos un carácter especial"

        return True, "Contraseña válida"

    @staticmethod
    def generate_secure_password(length: int = 12) -> str:
        """
        Generar una contraseña segura aleatoria
        """
        characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        return "".join(secrets.choice(characters) for _ in range(length))
