from fastapi import APIRouter, HTTPException, Query
from API.src.services.anime_service import AnimeService

router = APIRouter(prefix="/stream", tags=["Streaming"])
_anime = AnimeService()


@router.get("/home")
async def home():
    try:
        return await _anime.home()
    except Exception as e:
        raise HTTPException(502, detail=str(e))


@router.get("/search")
async def search(keyword: str = Query(..., min_length=1), page: int = 1):
    try:
        return await _anime.search(keyword, page)
    except Exception as e:
        raise HTTPException(502, detail=str(e))


@router.get("/suggest")
async def suggest(keyword: str = Query(..., min_length=1)):
    try:
        return await _anime.suggest(keyword)
    except Exception as e:
        raise HTTPException(502, detail=str(e))


@router.get("/filter")
async def filter_anime(
    keyword: str = None,
    tipo: str = None,
    estado: str = None,
    rating: str = None,
    score: str = None,
    season: str = None,
    language: str = None,
    genres: str = None,
    sort: str = None,
    page: int = 1,
):
    params = {k: v for k, v in {
        "keyword": keyword, "tipo": tipo, "estado": estado,
        "rating": rating, "score": score, "season": season,
        "language": language, "genres": genres, "sort": sort, "page": page,
    }.items() if v is not None}
    try:
        return await _anime.filter(params)
    except Exception as e:
        raise HTTPException(502, detail=str(e))


@router.get("/info")
async def info(id: str = Query(...)):
    try:
        return await _anime.info(id)
    except Exception as e:
        raise HTTPException(502, detail=str(e))


@router.get("/episodes/{anime_id}")
async def episodes(anime_id: str):
    try:
        return await _anime.episodes(anime_id)
    except Exception as e:
        raise HTTPException(502, detail=str(e))


@router.get("/servers")
async def servers(episodeId: str = Query(...)):
    try:
        return await _anime.servers(episodeId)
    except Exception as e:
        raise HTTPException(502, detail=str(e))


@router.get("/play")
async def play(
    id: str = Query(...),
    server: str = Query(default=""),
    type: str = Query(default="sub"),
):
    try:
        return await _anime.stream(id, server, type)
    except Exception as e:
        raise HTTPException(502, detail=str(e))


@router.get("/top")
async def top_ten():
    try:
        return await _anime.top_ten()
    except Exception as e:
        raise HTTPException(502, detail=str(e))


@router.get("/category/{name}")
async def category(name: str, page: int = 1):
    try:
        return await _anime.category(name, page)
    except Exception as e:
        raise HTTPException(502, detail=str(e))
