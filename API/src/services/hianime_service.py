import httpx
from API.src.core.config import get_settings


class HianimeService:
    def __init__(self):
        self._base = get_settings().hianime_api_url.rstrip("/")

    async def _get(self, path: str, params: dict = None) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self._base}{path}", params=params)
            r.raise_for_status()
            return r.json()

    async def home(self) -> dict:
        return await self._get("/api/")

    async def search(self, keyword: str, page: int = 1) -> dict:
        return await self._get("/api/search", {"keyword": keyword, "page": page})

    async def suggest(self, keyword: str) -> dict:
        return await self._get("/api/search/suggest", {"keyword": keyword})

    async def filter(self, params: dict) -> dict:
        return await self._get("/api/filter", params)

    async def info(self, anime_id: str) -> dict:
        return await self._get("/api/info", {"id": anime_id})

    async def episodes(self, anime_id: str) -> dict:
        return await self._get(f"/api/episodes/{anime_id}")

    async def servers(self, episode_id: str) -> dict:
        return await self._get(f"/api/servers/{episode_id}")

    async def stream(self, episode_id: str, server: str = "hd-1", sub_type: str = "sub") -> dict:
        return await self._get("/api/stream", {"id": episode_id, "server": server, "type": sub_type})

    async def top_ten(self) -> dict:
        return await self._get("/api/top-ten")

    async def category(self, name: str, page: int = 1) -> dict:
        return await self._get(f"/api/{name}", {"page": page})
