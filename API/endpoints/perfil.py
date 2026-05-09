from uuid import UUID
from typing import List
from pydantic import BaseModel
from typing import Optional

from API.src.crud.perfil_crud import PerfilCRUD
from API.database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from API.schemas import PerfilResponse
from sqlalchemy.orm import Session
from API.src.core.auth import get_current_user, CurrentUser

router = APIRouter(prefix="/perfil", tags=["Perfil"])


class PerfilCreateRequest(BaseModel):
    nombre_usuario: str
    avatar_url: Optional[str] = "av1"
    idioma: Optional[str] = "es"
    es_infantil: Optional[bool] = False


class PerfilUpdateRequest(BaseModel):
    nombre_usuario: Optional[str] = None
    avatar_url: Optional[str] = None
    idioma: Optional[str] = None
    es_infantil: Optional[bool] = None


@router.get("/", response_model=List[PerfilResponse])
async def obtener_todos_perfiles(db: Session = Depends(get_db)):
    return PerfilCRUD(db=db).obtener_todos_con_email()


@router.get("/usuario/{id_usuario}", response_model=List[PerfilResponse])
async def obtener_perfiles_por_usuario(id_usuario: UUID, db: Session = Depends(get_db)):
    perfiles = PerfilCRUD(db=db).obtener_perfiles_por_usuario(id_usuario=id_usuario)
    return perfiles


@router.get("/mis-perfiles", response_model=List[PerfilResponse])
async def mis_perfiles(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return PerfilCRUD(db=db).obtener_perfiles_por_usuario(id_usuario=current_user.id_usuario)


@router.post("/", response_model=PerfilResponse, status_code=status.HTTP_201_CREATED)
async def crear_perfil(
    datos: PerfilCreateRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    crud = PerfilCRUD(db=db)
    if crud.contar_perfiles_usuario(current_user.id_usuario) >= 4:
        raise HTTPException(status_code=400, detail="Límite de 4 perfiles por usuario alcanzado")
    perfil = crud.crear_perfil(
        nombre_usuario=datos.nombre_usuario,
        id_usuario=current_user.id_usuario,
        avatar_url=datos.avatar_url or "av1",
        idioma=datos.idioma or "es",
        es_infantil=datos.es_infantil or False,
    )
    if not perfil:
        raise HTTPException(status_code=400, detail="Nombre de perfil inválido o usuario no encontrado")
    return perfil


@router.put("/{perfil_id}", response_model=PerfilResponse)
async def actualizar_perfil(
    perfil_id: UUID,
    datos: PerfilUpdateRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    crud = PerfilCRUD(db=db)
    perfil = crud.obtener_perfil_por_id(perfil_id)
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    if perfil.id_usuario != current_user.id_usuario:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar este perfil")
    actualizado = crud.actualizar_perfil(perfil_id, datos.dict(exclude_none=True))
    if not actualizado:
        raise HTTPException(status_code=400, detail="Datos inválidos")
    return actualizado


@router.delete("/{perfil_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_perfil(
    perfil_id: UUID,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    crud = PerfilCRUD(db=db)
    perfil = crud.obtener_perfil_por_id(perfil_id)
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    if perfil.id_usuario != current_user.id_usuario:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este perfil")
    crud.eliminar_perfil(perfil_id)


@router.get("/{perfil_id}", response_model=PerfilResponse)
async def obtener_perfil(perfil_id: UUID, db: Session = Depends(get_db)):
    perfil = PerfilCRUD(db=db).obtener_perfil_por_id(perfil_id=perfil_id)
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return perfil
