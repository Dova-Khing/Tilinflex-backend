import asyncio
import httpx
from API.src.core.config import get_settings

ANILIST = "https://graphql.anilist.co"

_client: httpx.AsyncClient | None = None
_av1_url_cache: dict[str, str] = {}     # mal_id  → animeav1 URL
_anilist_mal_cache: dict[str, str] = {} # anilist_id → mal_id


def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=20)
    return _client


def _normalize(a: dict) -> dict:
    title  = a.get("title") or {}
    images = a.get("coverImage") or {}
    poster = images.get("extraLarge") or images.get("large") or ""
    banner = a.get("bannerImage") or poster

    trailer_url = ""
    if a.get("trailer"):
        t = a["trailer"]
        if t.get("site") == "youtube" and t.get("id"):
            trailer_url = f"https://www.youtube.com/watch?v={t['id']}"

    status_map = {
        "FINISHED":         "Finished Airing",
        "RELEASING":        "Currently Airing",
        "NOT_YET_RELEASED": "Not yet aired",
        "CANCELLED":        "Cancelled",
        "HIATUS":           "On Hiatus",
    }
    return {
        "id":          str(a.get("id", "")),
        "mal_id":      a.get("idMal"),
        "name":        title.get("english") or title.get("romaji") or "",
        "poster":      poster,
        "banner":      banner,
        "description": a.get("description") or "",
        "type":        (a.get("format") or "").replace("_", " ").title(),
        "episodes":    {"sub": a.get("episodes"), "dub": None},
        "score":       round(a["averageScore"] / 10, 2) if a.get("averageScore") else None,
        "status":      status_map.get(a.get("status", ""), a.get("status", "")),
        "year":        a.get("seasonYear"),
        "season":      (a.get("season") or "").capitalize(),
        "genres":      a.get("genres") or [],
        "studios":     ", ".join(n["name"] for n in (a.get("studios") or {}).get("nodes", [])),
        "duration":    f"{a['duration']} min" if a.get("duration") else "",
        "trailer":     trailer_url,
        "rank":        None,
    }


_MEDIA_FIELDS = """
  id idMal
  title { english romaji native }
  description(asHtml: false)
  coverImage { large extraLarge }
  bannerImage
  format episodes status season seasonYear averageScore
  genres duration trailer { id site }
  studios(isMain: true) { nodes { name } }
"""

# Para info() — sin studios para evitar conflicto con el query extendido
_INFO_FIELDS = """
  id idMal
  title { english romaji native }
  description(asHtml: false)
  coverImage { large extraLarge }
  bannerImage
  format episodes status season seasonYear averageScore
  genres duration trailer { id site }
"""


class AnimeService:

    # ── AniList GraphQL ────────────────────────────────────────────────────────

    async def _gql(self, query: str, variables: dict = None) -> dict:
        client = _get_client()
        for attempt in range(3):
            r = await client.post(
                ANILIST,
                json={"query": query, "variables": variables or {}},
                headers={"Content-Type": "application/json", "Accept": "application/json"},
            )
            if r.status_code == 429:
                await asyncio.sleep(min(int(r.headers.get("Retry-After", 30)), 30))
                continue
            r.raise_for_status()
            data = r.json()
            if "errors" in data:
                raise ValueError(data["errors"][0].get("message", "AniList error"))
            return data.get("data") or {}
        raise ValueError("AniList rate limit tras 3 intentos")

    # ── Anime1v-API ────────────────────────────────────────────────────────────

    async def _av1_get(self, path: str, params: dict = None) -> dict:
        s = get_settings()
        base = s.anime1v_url.rstrip("/")
        if not base:
            raise ValueError("ANIME1V_URL no configurada")
        client = _get_client()
        r = await client.get(f"{base}{path}", params={"apiKey": s.anime1v_key, **(params or {})})
        r.raise_for_status()
        return r.json()

    async def _get_mal_id(self, anilist_id: str) -> str | None:
        if anilist_id in _anilist_mal_cache:
            return _anilist_mal_cache[anilist_id]
        try:
            data = await self._gql(
                "query ($id: Int) { Media(id: $id, type: ANIME) { idMal } }",
                {"id": int(anilist_id)},
            )
            mal_id = (data.get("Media") or {}).get("idMal")
            if mal_id:
                _anilist_mal_cache[anilist_id] = str(mal_id)
                return str(mal_id)
        except Exception:
            pass
        return None

    async def _resolve_av1_url(self, mal_id: str) -> str | None:
        """mal_id → URL de animeav1.com, verificando malId para evitar falsos matches."""
        if mal_id in _av1_url_cache:
            return _av1_url_cache[mal_id]
        try:
            data = await self._gql(
                "query ($id: Int) { Media(idMal: $id, type: ANIME) { title { english romaji } } }",
                {"id": int(mal_id)},
            )
            title_obj = (data.get("Media") or {}).get("title") or {}
            title = title_obj.get("english") or title_obj.get("romaji")
            if not title:
                return None

            r = await self._av1_get("/api/v1/anime/search", {"q": title})
            results = (r.get("data") or {}).get("results") or []
            if not results:
                return None

            # Verificar malId — animeav1.com no siempre lo tiene, en ese caso aceptar igual
            target = int(mal_id)
            url = results[0].get("url") or ""
            if url:
                try:
                    info = await self._av1_get("/api/v1/anime/info", {"url": url})
                    info_mal = (info.get("data") or {}).get("malId")
                    if info_mal is None or int(info_mal) == target:
                        _av1_url_cache[mal_id] = url
                        return url
                except Exception:
                    pass
            return None
        except Exception:
            return None

    # ── Endpoints principales ──────────────────────────────────────────────────

    async def home(self) -> dict:
        data = await self._gql(f"""
            query {{
              trending: Page(page: 1, perPage: 8) {{
                media(sort: TRENDING_DESC, type: ANIME, isAdult: false) {{ {_MEDIA_FIELDS} }}
              }}
              airing: Page(page: 1, perPage: 15) {{
                media(sort: SCORE_DESC, type: ANIME, status: RELEASING, isAdult: false) {{ {_MEDIA_FIELDS} }}
              }}
              upcoming: Page(page: 1, perPage: 10) {{
                media(sort: POPULARITY_DESC, type: ANIME, status: NOT_YET_RELEASED, isAdult: false) {{ {_MEDIA_FIELDS} }}
              }}
              GenreCollection
            }}
        """)
        trending = [_normalize(a) for a in (data.get("trending") or {}).get("media", [])]
        airing   = [_normalize(a) for a in (data.get("airing")   or {}).get("media", [])]
        upcoming = [_normalize(a) for a in (data.get("upcoming") or {}).get("media", [])]
        genres   = [{"name": g, "id": g} for g in (data.get("GenreCollection") or [])]
        return {
            "spotlightAnimes":     trending,
            "trendingAnimes":      airing,
            "latestEpisodeAnimes": airing,
            "topUpcomingAnimes":   upcoming,
            "genres":              genres,
        }

    async def search(self, keyword: str, page: int = 1) -> dict:
        data = await self._gql(f"""
            query ($q: String, $page: Int) {{
              Page(page: $page, perPage: 20) {{
                pageInfo {{ lastPage }}
                media(search: $q, type: ANIME, isAdult: false, sort: SEARCH_MATCH) {{ {_MEDIA_FIELDS} }}
              }}
            }}
        """, {"q": keyword, "page": page})
        page_data = data.get("Page") or {}
        return {
            "animes":     [_normalize(a) for a in (page_data.get("media") or [])],
            "totalPages": (page_data.get("pageInfo") or {}).get("lastPage") or 1,
        }

    async def suggest(self, keyword: str) -> dict:
        data = await self._gql(f"""
            query ($q: String) {{
              Page(page: 1, perPage: 6) {{
                media(search: $q, type: ANIME, isAdult: false, sort: SEARCH_MATCH) {{ {_MEDIA_FIELDS} }}
              }}
            }}
        """, {"q": keyword})
        media = (data.get("Page") or {}).get("media") or []
        return {"data": {"suggestions": [_normalize(a) for a in media]}}

    async def filter(self, params: dict) -> dict:
        status_map = {
            "airing":   "RELEASING",
            "complete": "FINISHED",
            "upcoming": "NOT_YET_RELEASED",
        }
        sort_map = {
            "score":            ["SCORE_DESC"],
            "recently-updated": ["UPDATED_AT_DESC"],
            "name-az":          ["TITLE_ENGLISH"],
        }
        tipo_map = {
            "TV":      "TV",
            "Movie":   "MOVIE",
            "OVA":     "OVA",
            "ONA":     "ONA",
            "Special": "SPECIAL",
        }
        keyword = params.get("keyword") or None
        genre   = params.get("genres") or None
        status  = status_map.get(params.get("estado", "")) or None
        fmt     = tipo_map.get(params.get("tipo", "")) or None
        explicit_sort = params.get("sort", "")
        default_sort  = ["SEARCH_MATCH"] if keyword and not explicit_sort else ["POPULARITY_DESC"]
        sort = sort_map.get(explicit_sort, default_sort)

        # Construir query dinámico — AniList trata null explícito como filtro vacío
        var_defs   = ["$page: Int", "$sort: [MediaSort]"]
        media_args = ["type: ANIME", "isAdult: false", "sort: $sort"]
        variables  = {"page": params.get("page", 1), "sort": sort}

        if keyword:
            var_defs.append("$search: String");   media_args.append("search: $search");   variables["search"] = keyword
        if genre:
            var_defs.append("$genre: String");    media_args.append("genre: $genre");     variables["genre"]  = genre
        if status:
            var_defs.append("$status: MediaStatus"); media_args.append("status: $status"); variables["status"] = status
        if fmt:
            var_defs.append("$format: MediaFormat"); media_args.append("format: $format"); variables["format"] = fmt

        data = await self._gql(f"""
            query ({", ".join(var_defs)}) {{
              Page(page: $page, perPage: 20) {{
                pageInfo {{ lastPage }}
                media({", ".join(media_args)}) {{
                  {_MEDIA_FIELDS}
                }}
              }}
              GenreCollection
            }}
        """, variables)
        page_data = data.get("Page") or {}
        return {
            "animes":     [_normalize(a) for a in (page_data.get("media") or [])],
            "totalPages": (page_data.get("pageInfo") or {}).get("lastPage") or 1,
            "genres":     [{"name": g, "id": g} for g in (data.get("GenreCollection") or [])],
        }

    async def info(self, anime_id: str) -> dict:
        data = await self._gql(f"""
            query ($id: Int) {{
              Media(id: $id, type: ANIME) {{
                {_INFO_FIELDS}
                studios {{ nodes {{ name isAnimationStudio }} }}
                relations {{
                  edges {{
                    relationType(version: 2)
                    node {{
                      id idMal type format
                      title {{ english romaji }}
                      coverImage {{ large }}
                    }}
                  }}
                }}
              }}
            }}
        """, {"id": int(anime_id)})
        a = data.get("Media") or {}
        n = _normalize(a)

        all_studios = (a.get("studios") or {}).get("nodes", [])
        main_studios = [s["name"] for s in all_studios if s.get("isAnimationStudio")]
        producers    = [s["name"] for s in all_studios if not s.get("isAnimationStudio")]

        relations = [
            {
                "id":       str(node.get("id", "")),
                "mal_id":   node.get("idMal"),
                "name":     (node.get("title") or {}).get("english") or (node.get("title") or {}).get("romaji") or "",
                "poster":   (node.get("coverImage") or {}).get("large") or "",
                "relation": edge.get("relationType", ""),
                "format":   node.get("format", ""),
            }
            for edge in (a.get("relations") or {}).get("edges", [])
            if (node := edge.get("node") or {}) and node.get("type") == "ANIME"
        ]

        return {
            "data": {
                "anime": {
                    "info": {
                        "name":        n["name"],
                        "poster":      n["poster"],
                        "description": n["description"],
                        "stats":       {"type": n["type"], "rating": str(n["score"] or ""), "quality": ""},
                    },
                    "moreInfo": {
                        "japanese":  (a.get("title") or {}).get("native") or "",
                        "genres":    n["genres"],
                        "studios":   ", ".join(main_studios),
                        "producers": producers,
                        "duration":  n["duration"],
                        "status":    n["status"],
                        "premiered": f"{n['season']} {n['year'] or ''}".strip(),
                    },
                    "relations": relations,
                }
            }
        }

    async def episodes(self, anime_id: str) -> dict:
        mal_id = await self._get_mal_id(anime_id)
        av1_url: str | None = None

        if mal_id:
            av1_url = await self._resolve_av1_url(mal_id)

        # 1. anime1v info → episodes con URLs propias del sitio
        if av1_url:
            try:
                r = await self._av1_get("/api/v1/anime/info", {"url": av1_url})
                eps = (r.get("data") or {}).get("episodes") or []
                if eps:
                    return {"data": {"episodes": [
                        {
                            "episodeId": e["url"],
                            "number":    e["number"],
                            "title":     e.get("title") or f"Episodio {e['number']}",
                            "isFiller":  False,
                            "hasDub":    True,
                        }
                        for e in eps
                    ]}}
            except Exception:
                pass

        # 2. Jikan para metadata + URLs construidas con av1_url si está disponible
        if mal_id:
            try:
                client = _get_client()
                r = await client.get(f"https://api.jikan.moe/v4/anime/{mal_id}/episodes",
                                     timeout=10)
                if r.status_code == 200:
                    jikan_eps = r.json().get("data") or []
                    if jikan_eps:
                        return {"data": {"episodes": [
                            {
                                # Si tenemos av1_url usamos URLs reales de streaming
                                "episodeId": f"{av1_url}/{e.get('mal_id') or i + 1}"
                                             if av1_url else str(e.get("mal_id") or i + 1),
                                "number":    e.get("mal_id") or i + 1,
                                "title":     e.get("title") or f"Episodio {e.get('mal_id') or i + 1}",
                                "isFiller":  e.get("filler") or False,
                                "hasDub":    False,
                            }
                            for i, e in enumerate(jikan_eps)
                        ]}}
            except Exception:
                pass

        return {"data": {"episodes": []}}

    async def servers(self, episode_url: str) -> dict:
        try:
            r = await self._av1_get("/api/v1/anime/episode", {"url": episode_url})
            svrs = (r.get("data") or {}).get("servers") or {}

            def _map(lst):
                return [{"serverName": s["url"], "label": s.get("server", "Server")}
                        for s in (lst or []) if s.get("url")]

            return {"sub": _map(svrs.get("sub")), "dub": _map(svrs.get("dub")), "softsub": []}
        except Exception:
            return {"sub": [], "dub": [], "softsub": []}

    async def stream(self, episode_url: str, server: str = "", sub_type: str = "sub",
                     proxy_base: str = "") -> dict:
        if server and server.startswith("http"):
            return {"data": {"sources": [], "subtitles": [], "embedUrl": server}}
        try:
            r = await self._av1_get("/api/v1/anime/episode", {"url": episode_url})
            svrs = (r.get("data") or {}).get("servers") or {}
            server_list = svrs.get(sub_type.lower()) or svrs.get("sub") or []
            embed_url = server_list[0]["url"] if server_list else ""
            return {"data": {"sources": [], "subtitles": [], "embedUrl": embed_url}}
        except Exception as e:
            return {"data": {"sources": [], "subtitles": [], "message": str(e)}}

    async def top_ten(self) -> dict:
        data = await self._gql(f"""
            query {{
              Page(page: 1, perPage: 10) {{
                media(sort: TRENDING_DESC, type: ANIME, isAdult: false) {{ {_MEDIA_FIELDS} }}
              }}
            }}
        """)
        return {"trendingAnimes": [_normalize(a) for a in (data.get("Page") or {}).get("media", [])]}

    async def category(self, name: str, page: int = 1) -> dict:
        fmt_map = {"tv": "TV", "movie": "MOVIE", "ova": "OVA", "ona": "ONA", "special": "SPECIAL"}
        fmt = fmt_map.get(name.lower(), "TV")
        data = await self._gql(f"""
            query ($fmt: MediaFormat, $page: Int) {{
              Page(page: $page, perPage: 20) {{
                pageInfo {{ lastPage }}
                media(format: $fmt, type: ANIME, isAdult: false, sort: POPULARITY_DESC) {{ {_MEDIA_FIELDS} }}
              }}
            }}
        """, {"fmt": fmt, "page": page})
        page_data = data.get("Page") or {}
        return {
            "animes":     [_normalize(a) for a in (page_data.get("media") or [])],
            "totalPages": (page_data.get("pageInfo") or {}).get("lastPage") or 1,
        }
