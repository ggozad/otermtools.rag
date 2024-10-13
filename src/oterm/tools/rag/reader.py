import io
from pathlib import Path
from typing import ClassVar

import trafilatura
from docx import Document
from pypdf import PdfReader


class FileReader(object):

    extensions: ClassVar[list[str]] = [
        ".astro",
        ".c",
        ".cpp",
        ".css",
        ".csv",
        ".docx",
        ".go",
        ".h",
        ".hpp",
        ".html",
        ".java",
        ".js",
        ".json",
        ".kt",
        ".md",
        ".mdx",
        ".pdf",
        ".php",
        ".py",
        ".rb",
        ".rs",
        ".svelte",
        ".swift",
        ".ts",
        ".tsx",
        ".txt",
        ".vue",
    ]

    def read(self, path: Path) -> str:
        """
        Read a file and extract text.
        """
        with open(path, "rb") as file:
            bytes = file.read()
            if path.suffix == ".html":
                return self.from_html(bytes.decode("utf-8"))
            elif path.suffix == ".docx":
                return self.from_docx(bytes)
            elif path.suffix == ".pdf":
                return self.from_pdf(bytes)
            elif path.suffix in FileReader.extensions:
                return self.from_text(bytes.decode("utf-8"))
            else:
                raise ValueError(f"Unsupported file type: {path.suffix}")

    @staticmethod
    def from_docx(decoded_bytes: bytes) -> str:
        """Load and extract text from a Word document."""
        docx_bytes = io.BytesIO(decoded_bytes)
        reader = Document(docx_bytes)
        return "\n".join(paragraph.text for paragraph in reader.paragraphs)

    @staticmethod
    def from_pdf(decoded_bytes: bytes) -> str:
        """Extract text from a PDF document."""
        pdf_bytes = io.BytesIO(decoded_bytes)
        reader = PdfReader(pdf_bytes)
        return "\n\n".join(page.extract_text() for page in reader.pages)

    @staticmethod
    def from_html(html: str) -> str:
        """
        Convert HTML to plain text.
        """
        return trafilatura.extract(html, include_links=False) or ""

    @staticmethod
    def from_text(text: str) -> str:
        """
        Convert text to plain text.
        """
        return text
