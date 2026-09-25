"""
Second source -- different upstream, different JSON shape, proves the
registry generalizes. No search endpoint upstream, so search() falls back
to the listing rather than lying about supporting it.
"""
import requests

from app.sources.base import ResultPage, Source, Wallpaper

PAGE_SIZE = 30


class PicsumSource(Source):
    id = "picsum"
    name = "Lorem Picsum"
    base_url = "https://picsum.photos/v2/list"

    def _parse(self, payload: list[dict]) -> ResultPage:
        items = [
            Wallpaper(
                id=entry["id"],
                title=f"Photo by {entry['author']}",
                thumbnail_url=f"https://picsum.photos/id/{entry['id']}/300/200",
                full_url=entry["download_url"],
                source_page_url=entry["url"],
                width=entry.get("width"),
                height=entry.get("height"),
            )
            for entry in payload
        ]
        has_next_page = len(items) == PAGE_SIZE
        return ResultPage(items=items, has_next_page=has_next_page)

    def get_popular(self, page: int = 1) -> ResultPage:
        response = requests.get(
            self.base_url, params={"page": page, "limit": PAGE_SIZE}, timeout=10,
        )
        response.raise_for_status()
        return self._parse(response.json())

    def search(self, query: str, page: int = 1) -> ResultPage:
        return self.get_popular(page)