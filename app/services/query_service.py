from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.schemas.query import QueryResponse, SourceResponse
from app.services.embedding_service import generate_embedding
from app.services.llm_service import generate_answer
from app.services.vector_service import find_similar_chunks


def query_knowledge(db: Session, question: str):

    # Get all chunks
    chunks = db.query(Chunk).all()

    if not chunks:
        raise HTTPException(
            status_code=404,
            detail="No knowledge found. Please add a note or URL first."
        )

    # Generate embedding
    question_embedding = generate_embedding(question)

    # Find top relevant chunks
    top_chunks = find_similar_chunks(
        question_embedding,
        chunks,
        top_k=3
    )

    if not top_chunks:
        raise HTTPException(
            status_code=404,
            detail="No relevant information found for your question."
        )

    print("\n========== TOP MATCHES ==========")

    for item in top_chunks:
        print(f"Score: {item['score']:.4f}")
        print(item["chunk"].chunk_text[:300])
        print("--------------------------------")

    print("=================================\n")

    # Build context
    context = "\n\n---\n\n".join(
        item["chunk"].chunk_text
        for item in top_chunks
    )

    # Ask LLM
    answer = generate_answer(
        context=context,
        question=question
    )

    # Build sources
    sources = []

    for item in top_chunks:

        chunk = item["chunk"]

        sources.append(
            SourceResponse(
                source_type=chunk.item.source_type,
                original_source=chunk.item.original_source,
                created_at=chunk.item.created_at,
                snippet=chunk.chunk_text[:200] + "..."
            )
        )

    return QueryResponse(
        answer=answer,
        sources=sources
    )