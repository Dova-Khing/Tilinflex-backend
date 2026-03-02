"""
==============================
OPERACIONES CRUD PARA USUARIOS
==============================
Este módulo define las funciones necesarias
para realizar operaciones CRUD
(Crear, Leer, Actualizar, Eliminar)
en la tabla de usuarios de la base de datos.
Utiliza SQLAlchemy para interactuar
con la base de datos y Pydantic
para validar los datos de entrada y salida.
"""

import re
from uuid import UUID
from sqlalchemy import UUID
import pycountry
from sqlalchemy.orm import Session
from typing import List, Optional
from API.src.entities.usuarios import Usuario
import API.auth.security as PasswordManager


class validaciones_usuario:
    """
    Clase de validaciones para los datos del usuario.
    Contiene métodos estáticos para validar el formato del email,
    el país y la edad."""

    def validar_usuario(usuario: Usuario) -> bool:
        """
        Valida los datos del usuario.
        Retorna True si los datos son válidos, de lo contrario False.
        """
        if (
            not usuario.nombre
            or not usuario.apellido
            or not usuario.email
            or not usuario.pais
        ):
            print("Error: El nombre, apellido, email y país son campos obligatorios.")
            return False
        return True

    def validar_email(email: str) -> bool:
        """
        Valida el formato del email.
        Retorna True si el formato es válido, de lo contrario False.
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def validar_pais(pais: str) -> bool:
        """
        Valida que el país sea uno de los permitidos.
        Retorna True si el país es válido (América Latina, Estados Unidos, España), de lo contrario False.
        """
        # Códigos de países permitidos: América Latina, Estados Unidos y España
        paises_permitidos = [
            "AR",
            "BO",
            "BR",
            "CL",
            "CO",
            "CR",
            "CU",
            "EC",
            "SV",
            "GT",
            "GY",
            "HN",
            "NI",
            "PA",
            "PY",
            "PE",
            "DO",
            "SR",
            "UY",
            "VE",
            "US",
            "ES",
        ]

        try:
            # Buscar el país por nombre y obtener su código
            pais_obj = pycountry.countries.search_fuzzy(pais)
            if pais_obj:
                return pais_obj[0].alpha_2 in paises_permitidos
        except (AttributeError, LookupError):
            pass

        return False

    def validar_edad(edad: int) -> bool:
        """
        Valida que la edad sea un número positivo
        y mayor o igual a 18 años.
        Retorna True si la edad es válida, de lo contrario False.
        """
        try:
            if not isinstance(edad, int):
                print("Error: La edad debe ser un número entero.")
                return False
            if edad < 18:
                print("Error: La edad debe ser mayor o igual a 18 años.")
                return False
            return True
        except (TypeError, ValueError):
            print("Error: La edad debe ser un número entero y mayor o igual a 18.")
            return False

    def validar_nombre_apellido(nombre: str, apellido: str) -> bool:
        """
        Valida que el nombre y apellido no estén vacíos
        y contengan solo caracteres alfabéticos.
        Retorna True si el nombre y apellido son válidos, de lo contrario False.
        """
        if not nombre or not apellido:
            print("Error: El nombre y apellido no pueden estar vacíos.")
            return False
        if not re.match(r"^[a-zA-Z\s]+$", nombre):
            print(
                "Error: El nombre solo puede contener caracteres alfabéticos y espacios."
            )
            return False
        if not re.match(r"^[a-zA-Z\s]+$", apellido):
            print(
                "Error: El apellido solo puede contener caracteres alfabéticos y espacios."
            )
            return False
        return True


class UsuarioCRUD:
    """
    Clase que contiene métodos para realizar operaciones CRUD
    en la tabla de usuarios de la base de datos.
    """

    def __init__(self, db: Session):
        self.db = db

    def crear_usuario(self, usuario: Usuario) -> Optional[Usuario]:
        """
        Crea un nuevo usuario en la base de datos.
        Retorna el usuario creado o None si hubo un error.
        """
        if not validaciones_usuario.validar_usuario(usuario):
            return None
        if not validaciones_usuario.validar_email(usuario.email):
            print("Error: El formato del email es inválido.")
            return None
        if not validaciones_usuario.validar_pais(usuario.pais):
            print(
                "Error: El país no es válido. Debe ser de América Latina, Estados Unidos o España."
            )
            return None
        if not validaciones_usuario.validar_edad(usuario.edad):
            return None
        if not validaciones_usuario.validar_nombre_apellido(
            usuario.nombre, usuario.apellido
        ):
            return None

        nuevo_usuario = Usuario(
            nombre=usuario.nombre.strip().capitalize(),
            apellido=usuario.apellido.strip().capitalize(),
            email=usuario.email.lower().strip(),
            telefono=usuario.telefono,
            contrasena_hash=usuario.contrasena_hash,
            admin=usuario.admin,
            pais=usuario.pais,
            edad=usuario.edad,
        )

        self.db.add(nuevo_usuario)
        self.db.commit()
        self.db.refresh(nuevo_usuario)
        return nuevo_usuario

    def obtener_usuario(self, usuario_id: UUID) -> Optional[Usuario]:
        """Obtener un usuario por ID"""
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        """Obtener un usuario por email"""
        return (
            self.db.query(Usuario)
            .filter(Usuario.email == email.lower().strip())
            .first()
        )

    def obtener_usuario_por_telefono(self, telefono: str) -> Optional[Usuario]:
        """Obtener un usuario por teléfono"""
        return (
            self.db.query(Usuario).filter(Usuario.telefono == telefono.strip()).first()
        )

    def obtener_todos_usuarios(self) -> List[Usuario]:
        """Obtener todos los usuarios"""
        return self.db.query(Usuario).all()

    def autenticar_usuario(self, email: str, contrasena_hash: str) -> Optional[Usuario]:
        """Autenticar un usuario por email y contraseña"""
        usuario = self.obtener_usuario_por_email(email)

        if not usuario or not usuario.activo:
            print("Error: El usuario no existe o no está activo.")
            return None

        elif PasswordManager.verify_password(contrasena_hash, usuario.contrasena_hash):
            return usuario

        else:
            print("Error: Email o contraseña incorrectos.")
            return None

    def cambiar_contrasena(
        self, usuario_id: UUID, contrasena_actual: str, nueva_contrasena_hash: str
    ) -> bool:
        """Cambiar la contraseña de un usuario"""
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            print("Error: El usuario no existe.")
            return False

        if not PasswordManager.verify_password(
            contrasena_actual, usuario.contrasena_hash
        ):

            raise ValueError("La contraseña actual es incorrecta.")

        es_valida, mensaje = PasswordManager.validar_strength(nueva_contrasena_hash)

        if not es_valida:
            raise ValueError(f"Nueva contraseña invalida: {mensaje}")

        usuario.contrasena_hash = PasswordManager.hash_password(nueva_contrasena_hash)
        self.db.commit()
        return True

    def actualizar_usuario(self, usuario_id: UUID, **kwargs) -> Optional[Usuario]:
        """Actualizar un usuario con validaciones"""
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            print("Error: El usuario no existe.")
            return None

        if "email" in kwargs:
            email = kwargs["email"]
            if not validaciones_usuario.validar_email(email):
                raise ValueError("Email inválido")
            if (
                self.obtener_usuario_por_email(email)
                and self.obtener_usuario_por_email(email).id != usuario_id
            ):
                raise ValueError("El email ya está registrado")
            kwargs["email"] = email.lower().strip()

        if "telefono" in kwargs and kwargs["telefono"]:
            kwargs["telefono"] = kwargs["telefono"].strip()

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre es obligatorio")
            if len(nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
            kwargs["nombre"] = nombre.strip().capitalize()

        if "apellido" in kwargs:
            apellido = kwargs["apellido"]
            if not apellido or len(apellido.strip()) == 0:
                raise ValueError("El apellido es obligatorio")
            if len(apellido) > 100:
                raise ValueError("El apellido no puede exceder 100 caracteres")
            kwargs["apellido"] = apellido.strip().capitalize()

        if "contrasena" in kwargs:
            contrasena = kwargs["contrasena"]
            es_valida, mensaje = PasswordManager.validar_strength(contrasena)
            if not es_valida:
                raise ValueError(f"Contraseña inválida: {mensaje}")
            kwargs["contrasena_hash"] = PasswordManager.hash_password(contrasena)
            del kwargs["contrasena"]

        for key, value in kwargs.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)

        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def eliminar_usuario(self, usuario_id: UUID) -> bool:
        """Eliminar un usuario por ID"""
        usuario = self.obtener_usuario(usuario_id)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False

    def desactivar_usuario(self, usuario_id: UUID) -> Optional[Usuario]:
        """Desactivar un usuario (soft delete)"""
        return self.actualizar_usuario(usuario_id, activo=False)

    def obtener_usuarios_admin(self) -> List[Usuario]:
        """Obtener todos los usuarios administradores"""
        return self.db.query(Usuario).filter(Usuario.es_admin == True).all()

    def es_admin(self, usuario_id: UUID) -> bool:
        """Verificar si un usuario es administrador"""
        usuario = self.obtener_usuario(usuario_id)
        return usuario.es_admin if usuario else False

    def obtener_admin_por_defecto(self) -> Optional[Usuario]:
        """Obtener el usuario administrador por defecto"""
        return (
            self.db.query(Usuario)
            .filter(Usuario.email == "admin@system.com", Usuario.es_admin == True)
            .first()
        )
