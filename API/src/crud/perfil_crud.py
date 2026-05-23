import re
from sqlalchemy import func
from sqlalchemy.orm import Session
from API.src.entities.perfil import Perfil
from API.src.entities.usuarios import Usuario
from uuid import UUID
from typing import List, Optional


MAX_PERFILES = 4


class PerfilCRUD:

    def __init__(self, db: Session):
        self.db = db

    def _validar_nombre_usuario(self, nombre: str) -> bool:
        return bool(re.match(r"^[a-zA-Z0-9_]{3,20}$", nombre))

    # --- CREATE ---

    def crear_perfil(
        self,
        nombre_usuario: str,
        id_usuario: UUID,
        avatar_url: str = "av1",
        idioma: str = "es",
        es_infantil: bool = False,
    ) -> Perfil:
        if not self._validar_nombre_usuario(nombre_usuario):
            raise ValueError("Nombre de usuario inválido (3-20 chars, solo letras/números/guion_bajo)")

        if not self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first():
            raise ValueError("Usuario no encontrado")

        if self.contar_perfiles_usuario(id_usuario) >= MAX_PERFILES:
            raise ValueError("Límite de 4 perfiles por usuario alcanzado")

        perfil = Perfil(
            nombre_usuario=nombre_usuario,
            avatar_url=avatar_url,
            id_usuario=id_usuario,
            idioma=idioma,
            es_infantil=es_infantil,
        )
        self.db.add(perfil)
        self.db.commit()
        self.db.refresh(perfil)
        return perfil

    def contar_perfiles_usuario(self, id_usuario: UUID) -> int:
        return self.db.query(func.count(Perfil.id_perfil)).filter(Perfil.id_usuario == id_usuario).scalar()

    # --- READ ---

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
        return [
            {
                "id_perfil": p.id_perfil,
                "nombre_usuario": p.nombre_usuario,
                "avatar_url": p.avatar_url,
                "idioma": p.idioma,
                "es_infantil": p.es_infantil,
                "id_usuario": p.id_usuario,
                "fecha_creacion": p.fecha_creacion,
                "email_usuario": email,
            }
            for p, email in rows
        ]

    # --- UPDATE ---

    def actualizar_perfil(self, perfil_id: UUID, datos: dict) -> Optional[Perfil]:
        perfil = self.obtener_perfil_por_id(perfil_id)
        if not perfil:
            return None

        if "nombre_usuario" in datos and datos["nombre_usuario"]:
            if not self._validar_nombre_usuario(datos["nombre_usuario"]):
                raise ValueError("Nombre de usuario inválido")
            perfil.nombre_usuario = datos["nombre_usuario"]

        if datos.get("avatar_url"):
            perfil.avatar_url = datos["avatar_url"]

        if datos.get("idioma"):
            perfil.idioma = datos["idioma"]

        if "es_infantil" in datos and datos["es_infantil"] is not None:
            perfil.es_infantil = datos["es_infantil"]

        self.db.commit()
        self.db.refresh(perfil)
        return perfil

    # --- DELETE ---

    def eliminar_perfil(self, perfil_id: UUID) -> bool:
        perfil = self.obtener_perfil_por_id(perfil_id)
        if not perfil:
            return False
        self.db.delete(perfil)
        self.db.commit()
        return True
