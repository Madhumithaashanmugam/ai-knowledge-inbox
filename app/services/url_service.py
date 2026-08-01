import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException


def fetch_url_content(url: str):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "Chrome/138.0.0.0 Safari/537.36"
        )
    }

    try:
        response = httpx.get(
            url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=408,
            detail="The website took too long to respond."
        )

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Unable to fetch the URL. Website returned {e.response.status_code}."
        )

    except httpx.RequestError:
        raise HTTPException(
            status_code=400,
            detail="Unable to connect to the provided URL."
        )

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unnecessary elements
    for tag in soup([
        "script",
        "style",
        "nav",
        "header",
        "footer",
        "aside",
        "noscript",
        "svg",
        "form"
    ]):
        tag.decompose()

    # Prefer main/article content when available
    main = (
        soup.find("main")
        or soup.find("article")
        or soup.find(role="main")
    )

    if main:
        text = main.get_text(
            separator=" ",
            strip=True
        )
    else:
        text = soup.get_text(
            separator=" ",
            strip=True
        )

    # Clean whitespace
    text = " ".join(text.split())

    return text