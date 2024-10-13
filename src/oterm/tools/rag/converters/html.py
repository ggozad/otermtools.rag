import trafilatura


def from_html(html: str) -> str:
    """
    Convert HTML to plain text.
    """
    return trafilatura.extract(html, include_links=False) or ""
