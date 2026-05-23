import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from API.database.config import get_db
from API.dependencies import require_admin
from API.schemas import ObraCreate, ObraUpdate, ObraResponse
from API.src.crud.obras_crud import ObraCRUD
from API.src.services.anime_service import AnimeService


router = APIRouter(prefix="/obras", tags=["Obras"])


@router.get("/", response_model=List[ObraResponse])
def obtener_obras(db: Session = Depends(get_db)):
    return ObraCRUD(db).obtener_todas_obras()


@router.get("/{obra_id}", response_model=ObraResponse)
def obtener_obra(obra_id: UUID, db: Session = Depends(get_db)):
    obra = ObraCRUD(db).obtener_obra_por_id(obra_id)
    if not obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")
    return obra


@router.post("/importar/{anilist_id}", response_model=ObraResponse)
async def importar_desde_anilist(
    anilist_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Importa un anime de AniList a la BD de obras por su AniList ID. Si ya existe lo actualiza."""
    svc = AnimeService()
    try:
        r = await svc.info(str(anilist_id))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error al consultar AniList: {e}")

    anime = (r.get("data") or {}).get("anime") or {}
    info = anime.get("info") or {}
    more = anime.get("moreInfo") or {}

    if not info.get("name"):
        raise HTTPException(status_code=404, detail="Anime no encontrado en AniList")

    datos = {
        "mal_id":           None,
        "nombre":           info.get("name") or "",
        "nombre_japones":   more.get("japanese") or None,
        "descripcion":      info.get("description") or None,
        "tipo":             (info.get("stats") or {}).get("type") or None,
        "episodios":        None,
        "anio":             None,
        "temporada":        more.get("premiered") or None,
        "estado":           more.get("status") or None,
        "puntuacion":       float(info["stats"]["rating"]) if (info.get("stats") or {}).get("rating") else None,
        "rango":            None,
        "duracion":         more.get("duration") or None,
        "estudios":         more.get("studios") or None,
        "generos_externos": json.dumps(more.get("genres") or []),
        "thumbnail_url":    info.get("poster") or None,
        "banner_url":       info.get("poster") or None,
        "trailer_url":      None,
    }

    return ObraCRUD(db).upsert_desde_jikan(datos)


@router.post("/", response_model=ObraResponse)
def crear_obra(
    obra_data: ObraCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return ObraCRUD(db).crear_obra(**obra_data.dict())


@router.put("/{obra_id}", response_model=ObraResponse)
def actualizar_obra(
    obra_id: UUID,
    obra_data: ObraUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    obra = ObraCRUD(db).actualizar_obra(obra_id, obra_data.dict(exclude_none=True))
    if not obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")
    return obra


@router.delete("/{obra_id}")
def eliminar_obra(
    obra_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    if not ObraCRUD(db).eliminar_obra(obra_id):
        raise HTTPException(status_code=404, detail="Obra no encontrada")
    return {"mensaje": "Obra eliminada"}
