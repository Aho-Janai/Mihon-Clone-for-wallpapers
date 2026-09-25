"""
Mirrors Mihon's ExtensionLoader: discovers every Source implementation dropped
into this package. Drop a new file in app/sources/ with a Source subclass in
it and it shows up with zero changes anywhere else.
"""
import importlib
import inspect
import pkgutil

from app.sources.base import Source

_EXCLUDED_MODULES = {"base", "registry", "__init__"}


class SourceRegistry:
    def __init__(self):
        self._sources: dict[str, Source] = {}

    def discover(self) -> None:
        import app.sources as sources_pkg

        for _, module_name, _ in pkgutil.iter_modules(sources_pkg.__path__):
            if module_name in _EXCLUDED_MODULES:
                continue
            module = importlib.import_module(f"app.sources.{module_name}")
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, Source) and obj is not Source:
                    instance = obj()
                    self._sources[instance.id] = instance

    def all(self) -> list[Source]:
        return list(self._sources.values())

    def get(self, source_id: str) -> Source | None:
        return self._sources.get(source_id)


registry = SourceRegistry()