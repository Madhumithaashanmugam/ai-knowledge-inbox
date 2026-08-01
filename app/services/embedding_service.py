import ollama
from fastapi import HTTPException


def generate_embedding(text: str) -> list[float]:
    try:
        response = ollama.embed(
            model="nomic-embed-text",
            input=text
        )

        return response["embeddings"][0]

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to generate embedding. Please make sure Ollama is running."
        )


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    try:
        response = ollama.embed(
            model="nomic-embed-text",
            input=texts
        )

        return response["embeddings"]

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to generate embeddings. Please make sure Ollama is running."
        )