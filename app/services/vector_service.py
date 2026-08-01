import json

from sklearn.metrics.pairwise import cosine_similarity


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

    print("\n========== VECTOR SEARCH ==========")

    for item in scored_chunks[:10]:
        print(
            f"Score: {item['score']:.4f} | "
            f"{item['chunk'].chunk_text[:100]}"
        )

    print("===================================\n")

    # Remove weak matches
    filtered_chunks = [
        item
        for item in scored_chunks
        if item["score"] >= min_score
    ]

    return filtered_chunks[:top_k]