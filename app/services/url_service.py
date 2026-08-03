import logging

import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException

logger = logging.getLogger(__name__)


def fetch_url_content(url: str):

    logger.info("Fetching content from URL: %s", url)

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

        logger.info(
            "Successfully fetched URL. Status code: %d",
            response.status_code
        )

    except httpx.TimeoutException:
        logger.error("Timeout while fetching URL: %s", url)

        raise HTTPException(
            status_code=408,
            detail="The website took too long to respond."
        )

    except httpx.HTTPStatusError as e:
        logger.error(
            "HTTP error while fetching URL %s. Status code: %d",
            url,
            e.response.status_code
        )

        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Unable to fetch the URL. Website returned {e.response.status_code}."
        )

    except httpx.RequestError:
        logger.error("Unable to connect to URL: %s", url)

        raise HTTPException(
            status_code=400,
            detail="Unable to connect to the provided URL."
        )

    logger.info("Extracting webpage content.")

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
        logger.info("Using <main>/<article> content.")

        text = main.get_text(
            separator=" ",
            strip=True
        )
    else:
        logger.info("Main content not found. Falling back to full page text.")

        text = soup.get_text(
            separator=" ",
            strip=True
        )

    # Clean whitespace
    text = " ".join(text.split())

    logger.info(
        "Content extraction completed successfully. Extracted %d characters.",
        len(text)
    )

    return text