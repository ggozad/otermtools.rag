import hashlib
from mimetypes import guess_type
from pathlib import Path
from typing import Optional, Set

from otermtools.rag.logging import logger
from otermtools.rag.reader import FileReader
from otermtools.rag.store.engine import engine
from otermtools.rag.store.models.document import Document
from sqlmodel import Session, select
from watchfiles import Change, DefaultFilter, awatch


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
            if change == Change.added or change == Change.modified:
                await self._upsert_document(Path(path))
            elif change == Change.deleted:
                await self._delete_document(Path(path))

    async def refresh(self, paths: list[str | Path] | None = None):
        if paths is None:
            paths = self.paths
        for path in paths:
            for f in Path(path).rglob("**/*"):
                if f.is_file() and f.suffix in FileReader.extensions:
                    await self._upsert_document(f)

    async def _delete_document(self, file: Path):
        with Session(engine) as session:
            document = session.exec(
                select(Document).where(Document.uri == file.absolute().as_uri())
            ).first()
            if document:
                logger.info(f"Deleting document for {file}")
                session.delete(document)
                session.commit()

    async def _upsert_document(self, file: Path) -> Document | None:
        with Session(engine) as session:
            try:
                mimetype = guess_type(file.name)[0] or "unknown"
                document = session.exec(
                    select(Document).where(Document.uri == file.absolute().as_uri())
                ).first()
                md5 = hashlib.md5(file.read_bytes()).hexdigest()
                if not document:
                    logger.info(f"Creating document for {file}")
                    text = FileReader().read(file)
                    if not text:
                        return
                    document = Document(
                        text=text,
                        mimetype=mimetype,
                        uri=file.absolute().as_uri(),
                        meta={"md5": md5},
                    )
                elif document.meta.get("md5") == md5:
                    logger.info(f"Skipping {file}")
                    return document
                else:
                    logger.info(f"Updating document for {file}")
                    text = FileReader().read(file)
                    if not text:
                        session.delete(document)
                        return

                    document.text = text
                    meta = document.meta.copy()
                    meta["md5"] = md5
                    document.meta = meta

                document.chunks = []
                chunks = await document.chunk()
                document.chunks = chunks
                session.add(document)
                session.commit()
                session.refresh(document)
                return document
            except Exception as e:
                logger.error(f"Error processing {file}: {e}")
                raise e
