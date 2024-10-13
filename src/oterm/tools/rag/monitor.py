from pathlib import Path
from typing import Optional, Set

from watchfiles import Change, DefaultFilter, awatch

from oterm.tools.rag.logging import logger
from oterm.tools.rag.reader import FileReader


class FileFilter(DefaultFilter):

    def __init__(self, *, ignore_paths: Optional[list[str | Path]] = None) -> None:
        self.extensions = tuple(FileReader.extensions)
        super().__init__(ignore_paths=ignore_paths)

    def __call__(self, change: "Change", path: str) -> bool:
        return path.endswith(self.extensions) and super().__call__(change, path)


class FileWatcher:

    def __init__(self, paths: list[str | Path]):
        self.paths = paths

    async def observe(self):
        filter = FileFilter()
        logger.info(f"Watching {self.paths}")
        async for changes in awatch(*self.paths, watch_filter=filter):
            self.handler(changes)

    def handler(self, changes: Set[tuple[Change, str]]):
        for change in changes:
            logger.info(change)
