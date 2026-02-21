"""
CRUD PARA PERFIL
Un perfil representa la información de un usuario en el sistema.
"""
import re
from sqlalchemy.orm import Session
from entities.perfil import Perfil
from uuid import UUID
from typing import list, Optional
from .usuarios_crud import UsuariosCRUD


class validaciones_perfil:
    def __init__(self, db: Session):
        self.db = db

    def _validar_nombre_usuario(self, nombre_usuario: str) -> bool:
        """Validar formato de nombre de usuario"""
        pattern = r"^[a-zA-Z0-9_]{3,20}$"
        return re.match(pattern, nombre_usuario) is not None

    def _validar_id_usuario(self, id_usuario: UUID) -> bool:
        """Validar que el ID de usuario exista en la base de datos"""
        return UsuariosCRUD(self.db).obtener_usuario(id_usuario) is not None
