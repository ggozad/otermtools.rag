from mimetypes import guess_type
from pathlib import Path
from typing import Optional, Set

from sqlmodel import Session, select
from watchfiles import Change, DefaultFilter, awatch

from oterm.tools.rag.logging import logger
from oterm.tools.rag.reader import FileReader
from oterm.tools.rag.store.engine import engine
from oterm.tools.rag.store.models.document import Document


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
        await self.refresh()

        async for changes in awatch(*self.paths, watch_filter=filter):
            await self.handler(changes)

    async def handler(self, changes: Set[tuple[Change, str]]):
        for change, path in changes:
            logger.info(f'Observed "{change.name}" on {path}')
            await self._upsert_document(Path(path))

    async def refresh(self, paths: list[str | Path] | None = None):
        if paths is None:
            paths = self.paths
        for path in paths:
            for f in Path(path).rglob("**/*"):
                if f.is_file():
                    await self._upsert_document(f)

    async def _upsert_document(self, file: Path) -> Document:
        with Session(engine) as session:
            mimetype = guess_type(file.name)[0] or "unknown"
            document = session.exec(
                select(Document).where(Document.uri == file.absolute().as_uri())
            ).first()

            if not document:
                document = Document(
                    text=FileReader().read(file),
                    mimetype=mimetype,
                    uri=file.absolute().as_uri(),
                )
            else:
                document.text = FileReader().read(file)

            document.chunks = []
            chunks = await document.chunk()
            document.chunks = chunks
            session.add(document)
            session.commit()
            session.refresh(document)
            return document
