"""
Language-agnostic "Source" contract, modeled on Mihon's Source interface.
Every wallpaper provider implements this. Routes never talk to a specific
provider directly -- only through these methods.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Wallpaper:
    """Mirrors Mihon's SManga: a plain data holder, not tied to any one source's format."""
    id: str
    title: str
    thumbnail_url: str
    full_url: str
    source_page_url: str
    width: int | None = None
    height: int | None = None


@dataclass
class ResultPage:
    """Mirrors Mihon's MangasPage: a page of results plus a pagination flag."""
    items: list[Wallpaper]
    has_next_page: bool


class Source(ABC):
    """Mirrors Mihon's Source/HttpSource. id must be unique and stable."""
    id: str
    name: str
    requires_key: bool = False

    @abstractmethod
    def get_popular(self, page: int = 1) -> ResultPage:
        """Browse listing -- equivalent to Mihon's getPopularManga."""
        raise NotImplementedError

    @abstractmethod
    def search(self, query: str, page: int = 1) -> ResultPage:
        """Search listing -- equivalent to Mihon's getSearchManga."""
        raise NotImplementedError