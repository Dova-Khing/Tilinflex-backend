import asyncio
import httpx
from API.src.core.config import get_settings

JIKAN = "https://api.jikan.moe/v4"


def _normalize(a: dict) -> dict:
    """Convierte objeto Jikan al formato estándar que usa el front."""
    return {
        "id":          str(a.get("mal_id", "")),
        "name":        a.get("title_english") or a.get("title") or "",
        "poster":      (a.get("images") or {}).get("jpg", {}).get("large_image_url") or
                       (a.get("images") or {}).get("jpg", {}).get("image_url") or "",
        "banner":      (a.get("images") or {}).get("jpg", {}).get("large_image_url") or "",
        "description": a.get("synopsis") or "",
        "type":        a.get("type") or "",
        "episodes":    {"sub": a.get("episodes"), "dub": None},
        "score":       a.get("score"),
        "status":      a.get("status") or "",
        "year":        a.get("year"),
        "season":      a.get("season") or "",
        "genres":      [g["name"] for g in (a.get("genres") or [])],
        "studios":     ", ".join(s["name"] for s in (a.get("studios") or [])),
        "duration":    a.get("duration") or "",
        "trailer":     (a.get("trailer") or {}).get("url") or "",
        "rank":        a.get("rank"),
        "mal_id":      a.get("mal_id"),
    }


class AnimeService:

    async def _get(self, path: str, params: dict = None) -> dict:
        for attempt in range(3):
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.get(f"{JIKAN}{path}", params=params)
                if r.status_code == 429:
                    await asyncio.sleep(1.5 * (attempt + 1))
                    continue
                r.raise_for_status()
                return r.json()
        raise httpx.HTTPStatusError("Rate limit tras 3 intentos", request=r.request, response=r)

    async def home(self) -> dict:
        import asyncio
        # Dos lotes de 2 para respetar rate limit de Jikan (3 req/s)
        top, airing = await asyncio.gather(
            self._get("/top/anime", {"limit": 10, "filter": "bypopularity"}),
            self._get("/seasons/now", {"limit": 24}),
        )
        await asyncio.sleep(0.4)
        upcoming, genres_r = await asyncio.gather(
            self._get("/seasons/upcoming", {"limit": 10}),
            self._get("/genres/anime"),
        )

        MAIN_TYPES = {"TV", "Movie", "ONA"}
        airing_data = [a for a in (airing.get("data") or []) if a.get("type") in MAIN_TYPES]

        spotlight = [_normalize(a) for a in (top.get("data") or [])[:8]]
        trending  = [_normalize(a) for a in airing_data[:15]]
        latest    = [_normalize(a) for a in airing_data]
        upcoming_ = [_normalize(a) for a in (upcoming.get("data") or [])]
        genres = [{"name": g["name"], "id": g["mal_id"]} for g in (genres_r.get("data") or [])]
        return {
            "spotlightAnimes":     spotlight,
            "trendingAnimes":      trending,
            "latestEpisodeAnimes": latest,
            "topUpcomingAnimes":   upcoming_,
            "genres":              genres,
        }

    async def search(self, keyword: str, page: int = 1) -> dict:
        r = await self._get("/anime", {"q": keyword, "page": page, "limit": 20})
        return {
            "animes":     [_normalize(a) for a in (r.get("data") or [])],
            "totalPages": (r.get("pagination") or {}).get("last_visible_page") or 1,
        }

    async def suggest(self, keyword: str) -> dict:
        r = await self._get("/anime", {"q": keyword, "limit": 6})
        return {
            "data": {
                "suggestions": [_normalize(a) for a in (r.get("data") or [])]
            }
        }

    async def filter(self, params: dict) -> dict:
        jikan_params: dict = {"page": params.get("page", 1), "limit": 20}
        if params.get("keyword"): jikan_params["q"]        = params["keyword"]
        if params.get("tipo"):    jikan_params["type"]     = params["tipo"].lower()
        if params.get("genres"):  jikan_params["genres"]   = params["genres"]
        if params.get("sort") == "score":             jikan_params["order_by"] = "score";  jikan_params["sort"] = "desc"
        if params.get("sort") == "recently-updated":  jikan_params["order_by"] = "start_date"; jikan_params["sort"] = "desc"
        if params.get("sort") == "name-az":           jikan_params["order_by"] = "title";  jikan_params["sort"] = "asc"
        estado = params.get("estado", "")
        if estado == "airing":   jikan_params["status"] = "airing"
        if estado == "complete": jikan_params["status"] = "complete"
        if estado == "upcoming": jikan_params["status"] = "upcoming"
        r = await self._get("/anime", jikan_params)
        await asyncio.sleep(0.4)
        genres_r = await self._get("/genres/anime")
        return {
            "animes":     [_normalize(a) for a in (r.get("data") or [])],
            "totalPages": (r.get("pagination") or {}).get("last_visible_page") or 1,
            "genres":     [{"name": g["name"], "id": g["mal_id"]} for g in (genres_r.get("data") or [])],
        }

    async def info(self, anime_id: str) -> dict:
        r = await self._get(f"/anime/{anime_id}/full")
        a = r.get("data") or {}
        n = _normalize(a)
        return {
            "data": {
                "anime": {
                    "info": {
                        "name":        n["name"],
                        "poster":      n["poster"],
                        "description": n["description"],
                        "stats": {
                            "type":    n["type"],
                            "rating":  str(a.get("score") or ""),
                            "quality": "",
                        },
                    },
                    "moreInfo": {
                        "japanese":  a.get("title_japanese") or "",
                        "genres":    n["genres"],
                        "studios":   n["studios"],
                        "producers": [p["name"] for p in (a.get("producers") or [])],
                        "duration":  n["duration"],
                        "status":    n["status"],
                        "premiered": f"{a.get('season','').capitalize()} {a.get('year','') or ''}".strip(),
                    },
                }
            }
        }

    async def episodes(self, anime_id: str) -> dict:
        r = await self._get(f"/anime/{anime_id}/episodes")
        eps = [
            {
                "episodeId": str(e.get("mal_id") or e.get("id") or i),
                "number":    e.get("mal_id") or i + 1,
                "title":     e.get("title") or f"Episodio {e.get('mal_id') or i+1}",
                "isFiller":  e.get("filler") or False,
            }
            for i, e in enumerate(r.get("data") or [])
        ]
        return {"data": {"episodes": eps}}

    async def servers(self, episode_id: str) -> dict:
        return {"sub": [{"serverName": "default"}]}

    async def stream(self, episode_id: str, server: str = "default", sub_type: str = "sub") -> dict:
        return {
            "data": {
                "sources":   [],
                "subtitles": [],
                "message":   "Streaming no disponible — integración pendiente",
            }
        }

    async def top_ten(self) -> dict:
        r = await self._get("/top/anime", {"limit": 10})
        return {"trendingAnimes": [_normalize(a) for a in (r.get("data") or [])]}

    async def category(self, name: str, page: int = 1) -> dict:
        r = await self._get("/anime", {"type": name.lower(), "page": page, "limit": 20})
        return {
            "animes":     [_normalize(a) for a in (r.get("data") or [])],
            "totalPages": (r.get("pagination") or {}).get("last_visible_page") or 1,
        }
