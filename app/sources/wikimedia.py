"""
Third source -- Wikimedia Commons, via the public MediaWiki API. No key
required, but Wikimedia's API asks for a descriptive User-Agent on every
request, or you risk getting throttled/blocked.

MediaWiki's native pagination is continuation-token based, not page-number
based -- but the search generator also accepts a numeric offset (gsroffset),
so this uses that to keep the same page: int contract as the other sources.
"""
import requests

from app.sources.base import ResultPage, Source, Wallpaper

PAGE_SIZE = 30
USER_AGENT = "MihonCloneWallpapers/0.1 (POC; contact: msmangekyou49@gmail.com)"


class WikimediaSource(Source):
    id = "wikimedia"
    name = "Wikimedia Commons"
    base_url = "https://commons.wikimedia.org/w/api.php"

    def _query(self, search_term: str, page: int) -> ResultPage:
        params = {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": f"filetype:bitmap {search_term}",
            "gsrnamespace": 6,          # File namespace
            "gsroffset": (page - 1) * PAGE_SIZE,
            "gsrlimit": PAGE_SIZE,
            "prop": "imageinfo",
            "iiprop": "url|size",
            "iiurlwidth": 300,
        }
        response = requests.get(
            self.base_url,
            params=params,
            headers={"User-Agent": USER_AGENT},
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()

        pages = payload.get("query", {}).get("pages", {})
        items = []
        for page_data in pages.values():
            infos = page_data.get("imageinfo")
            if not infos:
                continue
            info = infos[0]
            items.append(
                Wallpaper(
                    id=str(page_data["pageid"]),
                    title=page_data["title"].removeprefix("File:"),
                    thumbnail_url=info.get("thumburl", info["url"]),
                    full_url=info["url"],
                    source_page_url=info["descriptionurl"],
                    width=info.get("width"),
                    height=info.get("height"),
                )
            )

        has_next_page = "continue" in payload
        return ResultPage(items=items, has_next_page=has_next_page)

    def get_popular(self, page: int = 1) -> ResultPage:
        return self._query("wallpaper", page)

    def search(self, query: str, page: int = 1) -> ResultPage:
        return self._query(query, page)