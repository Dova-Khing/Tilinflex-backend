"""
CRUD PARA PERFIL
Un perfil representa la información de un usuario en el sistema.
"""

import re
from sqlalchemy.orm import Session
from API.src.entities.perfil import Perfil
from uuid import UUID
from typing import List, Optional
from .usuarios_crud import UsuarioCRUD
from API.src.entities.usuarios import Usuario


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
        return UsuarioCRUD(self.db).obtener_usuario(id_usuario) is not None

    # -----------------------------------
    # CREATE
    # -----------------------------------


    MAX_PERFILES = 4

    def crear_perfil(
        self,
        nombre_usuario: str,
        id_usuario: UUID,
        avatar_url: str = "av1",
        idioma: str = "es",
        es_infantil: bool = False,
    ) -> Optional[Perfil]:
        if not self._validar_nombre_usuario(nombre_usuario):
            return None

        if not self._validar_id_usuario(id_usuario):
            return None

        existentes = self.obtener_perfiles_por_usuario(id_usuario)
        if len(existentes) >= self.MAX_PERFILES:
            return None

        nuevo_perfil = Perfil(
            nombre_usuario=nombre_usuario,
            avatar_url=avatar_url,
            id_usuario=id_usuario,
            idioma=idioma,
            es_infantil=es_infantil,
        )

        self.db.add(nuevo_perfil)
        self.db.commit()
        self.db.refresh(nuevo_perfil)

        return nuevo_perfil

    def contar_perfiles_usuario(self, id_usuario: UUID) -> int:
        return len(self.obtener_perfiles_por_usuario(id_usuario))

    # -----------------------------------
    # READ
    # -----------------------------------

    def obtener_perfil_por_id(self, perfil_id: UUID) -> Optional[Perfil]:
        return self.db.query(Perfil).filter(Perfil.id_perfil == perfil_id).first()

    def obtener_perfiles_por_usuario(self, id_usuario: UUID) -> List[Perfil]:
        return self.db.query(Perfil).filter(Perfil.id_usuario == id_usuario).all()

    def obtener_todos(self) -> List[Perfil]:
        return self.db.query(Perfil).all()

    def obtener_todos_con_email(self) -> List[dict]:
        rows = (
            self.db.query(Perfil, Usuario.email)
            .join(Usuario, Perfil.id_usuario == Usuario.id_usuario)
            .all()
        )
        result = []
        for perfil, email in rows:
            result.append({
                "id_perfil": perfil.id_perfil,
                "nombre_usuario": perfil.nombre_usuario,
                "avatar_url": perfil.avatar_url,
                "idioma": perfil.idioma,
                "es_infantil": perfil.es_infantil,
                "id_usuario": perfil.id_usuario,
                "fecha_creacion": perfil.fecha_creacion,
                "email_usuario": email,
            })
        return result

    def obtener_todos_usuarios(self) -> List[Usuario]:
        """Obtener todos los usuarios"""
        return self.db.query(Usuario).all()

    # -----------------------------------
    # UPDATE
    # -----------------------------------

    def actualizar_perfil(self, perfil_id: UUID, datos: dict) -> Optional[Perfil]:
        perfil = self.obtener_perfil_por_id(perfil_id)
        if not perfil:
            return None

        if "nombre_usuario" in datos and datos["nombre_usuario"]:
            if not self._validar_nombre_usuario(datos["nombre_usuario"]):
                return None
            perfil.nombre_usuario = datos["nombre_usuario"]

        if "avatar_url" in datos and datos["avatar_url"]:
            perfil.avatar_url = datos["avatar_url"]

        if "idioma" in datos and datos["idioma"]:
            perfil.idioma = datos["idioma"]

        if "es_infantil" in datos and datos["es_infantil"] is not None:
            perfil.es_infantil = datos["es_infantil"]

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
