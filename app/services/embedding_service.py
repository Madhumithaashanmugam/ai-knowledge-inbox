import logging

import ollama
from fastapi import HTTPException

# Configure logger
logger = logging.getLogger(__name__)


def generate_embedding(text: str) -> list[float]:
    try:
        logger.info("Generating embedding for a single text.")
        logger.debug("Input text length: %d", len(text))
        logger.debug("Input preview: %s", text[:100])

        response = ollama.embed(
            model="nomic-embed-text",
            input=text
        )

        embeddings = response["embeddings"]

        logger.info("Embedding generated successfully.")
        logger.debug("Embedding dimension: %d", len(embeddings[0]))

        return embeddings[0]

    except Exception as e:
        logger.exception("Failed to generate embedding: %s", str(e))

        raise HTTPException(
            status_code=503,
            detail="Unable to generate embedding. Please make sure Ollama is running."
        )


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    try:
        logger.info("Generating embeddings for %d text chunks.", len(texts))

        if texts:
            logger.debug("First chunk preview: %s", texts[0][:100])

        response = ollama.embed(
            model="nomic-embed-text",
            input=texts
        )

        embeddings = response["embeddings"]

        logger.info("Successfully generated %d embeddings.", len(embeddings))

        if embeddings:
            logger.debug("Embedding dimension: %d", len(embeddings[0]))

        return embeddings

    except Exception as e:
        logger.exception("Failed to generate embeddings: %s", str(e))

        raise HTTPException(
            status_code=503,
            detail="Unable to generate embeddings. Please make sure Ollama is running."
        )