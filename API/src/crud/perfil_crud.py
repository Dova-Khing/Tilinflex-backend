"""
CRUD PARA PERFIL
Un perfil representa la información de un usuario en el sistema.
"""

import re
from sqlalchemy.orm import Session
from entities.perfil import Perfil
from uuid import UUID
from typing import List, Optional
from .usuarios_crud import UsuariosCRUD


class PerfilCRUD:

    def __init__(self, db: Session):
        self.db = db

    # -----------------------------------
    # VALIDACIONES
    # -----------------------------------

    def _validar_nombre_usuario(self, nombre_usuario: str) -> bool:
        """Validar formato de nombre de usuario"""
        pattern = r"^[a-zA-Z0-9_]{3,20}$"
        return re.match(pattern, nombre_usuario) is not None

    def _validar_id_usuario(self, id_usuario: UUID) -> bool:
        """Validar que el usuario exista"""
        return UsuariosCRUD(self.db).obtener_usuario(id_usuario) is not None

    # -----------------------------------
    # CREATE
    # -----------------------------------

    def crear_perfil(self, nombre_usuario: str, id_usuario: UUID) -> Optional[Perfil]:
        """Crear un nuevo perfil"""

        # Validar nombre
        if not self._validar_nombre_usuario(nombre_usuario):
            return None

        # Validar usuario existente
        if not self._validar_id_usuario(id_usuario):
            return None

        nuevo_perfil = Perfil(nombre_usuario=nombre_usuario, id_usuario=id_usuario)

        self.db.add(nuevo_perfil)
        self.db.commit()
        self.db.refresh(nuevo_perfil)

        return nuevo_perfil

    # -----------------------------------
    # READ
    # -----------------------------------

    def obtener_perfil_por_id(self, perfil_id: UUID) -> Optional[Perfil]:
        return self.db.query(Perfil).filter(Perfil.id_perfil == perfil_id).first()

    def obtener_perfiles_por_usuario(self, id_usuario: UUID) -> List[Perfil]:
        return self.db.query(Perfil).filter(Perfil.id_usuario == id_usuario).all()

    def obtener_todos(self) -> List[Perfil]:
        return self.db.query(Perfil).all()

    # -----------------------------------
    # UPDATE
    # -----------------------------------

    def actualizar_perfil(self, perfil_id: UUID, nuevo_nombre: str) -> Optional[Perfil]:
        """Actualizar nombre de perfil"""

        perfil = self.obtener_perfil_por_id(perfil_id)

        if not perfil:
            return None

        if not self._validar_nombre_usuario(nuevo_nombre):
            return None

        perfil.nombre_usuario = nuevo_nombre

        self.db.commit()
        self.db.refresh(perfil)

        return perfil

    # -----------------------------------
    # DELETE
    # -----------------------------------

    def eliminar_perfil(self, perfil_id: UUID) -> bool:
        """Eliminar perfil"""

        perfil = self.obtener_perfil_por_id(perfil_id)

        if not perfil:
            return False

        self.db.delete(perfil)
        self.db.commit()

        return True
