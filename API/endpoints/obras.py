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


@router.post("/importar/{mal_id}", response_model=ObraResponse)
async def importar_desde_jikan(
    mal_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Importa un anime de Jikan/MAL a la BD de obras. Si ya existe lo actualiza."""
    svc = AnimeService()
    try:
        r = await svc._get(f"/anime/{mal_id}/full")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error al consultar Jikan: {e}")

    a = r.get("data") or {}
    if not a:
        raise HTTPException(status_code=404, detail="Anime no encontrado en Jikan")

    datos = {
        "mal_id":           a.get("mal_id"),
        "nombre":           a.get("title_english") or a.get("title") or "",
        "nombre_japones":   a.get("title_japanese") or None,
        "descripcion":      a.get("synopsis") or None,
        "tipo":             a.get("type") or None,
        "episodios":        a.get("episodes") or None,
        "anio":             a.get("year") or None,
        "temporada":        a.get("season") or None,
        "estado":           a.get("status") or None,
        "puntuacion":       a.get("score") or None,
        "rango":            a.get("rank") or None,
        "duracion":         a.get("duration") or None,
        "estudios":         ", ".join(s["name"] for s in (a.get("studios") or [])) or None,
        "generos_externos": json.dumps([g["name"] for g in (a.get("genres") or [])]),
        "thumbnail_url":    (a.get("images") or {}).get("jpg", {}).get("large_image_url") or None,
        "banner_url":       (a.get("images") or {}).get("jpg", {}).get("large_image_url") or None,
        "trailer_url":      (a.get("trailer") or {}).get("url") or None,
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
