import json

from sqlalchemy.orm import Session

from app.models.chunk import Chunk
from app.models.item import Item
from app.schemas.item import ItemCreate, SourceType
from app.services.chunk_service import create_chunks
from app.services.embedding_service import generate_embeddings
from app.services.llm_service import generate_summary, generate_title
from app.services.url_service import fetch_url_content


def create_item(db: Session, item: ItemCreate):

    original_source = None
    content = item.content

    # Fetch webpage if URL
    if item.source_type == SourceType.url:
        original_source = item.content
        content = fetch_url_content(item.content)

    # Generate AI metadata
    title = generate_title(content)
    summary = generate_summary(content)

    # Save item
    db_item = Item(
        source_type=item.source_type,
        original_source=original_source,
        title=title,
        summary=summary,
        content=content
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    # Create chunks
    chunks = create_chunks(content)

    # Generate embeddings in one request
    embeddings = generate_embeddings(chunks)

    chunk_objects = []

    for chunk_text, embedding in zip(chunks, embeddings):
        chunk_objects.append(
            Chunk(
                item_id=db_item.id,
                chunk_text=chunk_text,
                embedding=json.dumps(embedding)
            )
        )

    # Bulk insert
    db.bulk_save_objects(chunk_objects)
    db.commit()

    return db_item


def get_items(
    db: Session,
    page: int = 1,
    limit: int = 9
):
    offset = (page - 1) * limit

    return (
        db.query(Item)
        .order_by(Item.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )