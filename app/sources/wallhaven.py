"""
API-backed source. Mirrors Mihon's HttpSource: base_url + request -> parse
JSON -> build Wallpaper objects.
"""
import requests

from app.sources.base import ResultPage, Source, Wallpaper


class WallhavenSource(Source):
    id = "wallhaven"
    name = "Wallhaven"
    base_url = "https://wallhaven.cc/api/v1/search"

    def _parse(self, payload: dict) -> ResultPage:
        items = [
            Wallpaper(
                id=entry["id"],
                title=entry["id"],  # Wallhaven doesn't title wallpapers
                thumbnail_url=entry["thumbs"]["small"],
                full_url=entry["path"],
                source_page_url=entry["url"],
                width=entry.get("dimension_x"),
                height=entry.get("dimension_y"),
            )
            for entry in payload["data"]
        ]
        meta = payload.get("meta", {})
        has_next_page = meta.get("current_page", 1) < meta.get("last_page", 1)
        return ResultPage(items=items, has_next_page=has_next_page)

    def get_popular(self, page: int = 1) -> ResultPage:
        response = requests.get(
            self.base_url, params={"sorting": "toplist", "page": page}, timeout=10,
        )
        response.raise_for_status()
        return self._parse(response.json())

    def search(self, query: str, page: int = 1) -> ResultPage:
        response = requests.get(
            self.base_url, params={"q": query, "page": page}, timeout=10,
        )
        response.raise_for_status()
        return self._parse(response.json())