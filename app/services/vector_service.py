import json
import logging

from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


def find_similar_chunks(
    question_embedding,
    chunks,
    top_k: int = 3,
    min_score: float = 0.45
):
    """
    Find the most semantically similar chunks using cosine similarity.

    Args:
        question_embedding: Embedding of the user's question.
        chunks: List of Chunk ORM objects.
        top_k: Maximum number of chunks to return.
        min_score: Minimum similarity score required.

    Returns:
        List of dictionaries:
        [
            {
                "chunk": Chunk,
                "score": 0.91
            }
        ]
    """

    logger.info(
        "Starting vector search across %d chunks.",
        len(chunks)
    )

    scored_chunks = []

    for chunk in chunks:

        chunk_embedding = json.loads(chunk.embedding)

        score = cosine_similarity(
            [question_embedding],
            [chunk_embedding]
        )[0][0]

        scored_chunks.append(
            {
                "chunk": chunk,
                "score": float(score)
            }
        )

    # Highest similarity first
    scored_chunks.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    logger.info("Top similarity scores:")

    for index, item in enumerate(scored_chunks[:10], start=1):
        logger.info(
            "Rank %d | Score: %.4f",
            index,
            item["score"]
        )

    # Remove weak matches
    filtered_chunks = [
        item
        for item in scored_chunks
        if item["score"] >= min_score
    ]

    logger.info(
        "%d chunks passed the similarity threshold of %.2f.",
        len(filtered_chunks),
        min_score
    )

    logger.info(
        "Returning top %d matching chunks.",
        min(top_k, len(filtered_chunks))
    )

    return filtered_chunks[:top_k]