import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.schemas.query import QueryResponse, SourceResponse
from app.services.embedding_service import generate_embedding
from app.services.llm_service import generate_answer
from app.services.vector_service import find_similar_chunks

logger = logging.getLogger(__name__)


def query_knowledge(db: Session, question: str):

    logger.info("Received query: %s", question)

    # Get all chunks
    chunks = db.query(Chunk).all()

    logger.info("Loaded %d chunks from the database.", len(chunks))

    if not chunks:
        logger.warning("No knowledge found in the database.")

        raise HTTPException(
            status_code=404,
            detail="No knowledge found. Please add a note or URL first."
        )

    # Generate embedding
    logger.info("Generating embedding for the user's question.")

    question_embedding = generate_embedding(question)

    # Find top relevant chunks
    logger.info("Searching for the top matching chunks.")

    top_chunks = find_similar_chunks(
        question_embedding,
        chunks,
        top_k=5
    )

    if not top_chunks:
        logger.warning("No relevant chunks found for the question.")

        raise HTTPException(
            status_code=404,
            detail="No relevant information found for your question."
        )

    logger.info("Top %d matching chunks found.", len(top_chunks))

    for index, item in enumerate(top_chunks, start=1):
        logger.info(
            "Match %d | Score: %.4f",
            index,
            item["score"]
        )

    # Build context
    context = "\n\n---\n\n".join(
        item["chunk"].chunk_text
        for item in top_chunks
    )

    logger.info("Context prepared for LLM.")

    # Ask LLM
    logger.info("Generating AI answer.")

    answer = generate_answer(
        context=context,
        question=question
    )

    logger.info("AI answer generated successfully.")

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

    logger.info("Prepared %d source references.", len(sources))
    logger.info("Query completed successfully.")

    return QueryResponse(
        answer=answer,
        sources=sources
    )