from urllib.parse import urlparse

from bs4 import BeautifulSoup
from fastapi import HTTPException


def verify_url(url: str) -> bool:
    """
    Verify if the provided URL is valid and accessible.
    """
    parsed_url = urlparse(url)
    if not (parsed_url.scheme in ["http", "https"] and parsed_url.netloc):
        raise HTTPException(status_code=400, detail="Invalid URL provided")


def sanitize_html(html_content: str) -> str:
    """
    Sanitize HTML content by removing scripts, styles, and other non-visible elements.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    for script_or_style in soup(["script", "style", "noscript"]):
        script_or_style.decompose()
    visible_text = soup.get_text(separator=" ", strip=True)
    sanitized_text = " ".join(visible_text.split())
    return sanitized_text
