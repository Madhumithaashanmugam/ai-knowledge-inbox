from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)

    # text | url
    source_type = Column(String, nullable=False)

    # Original URL (only for URL items)
    original_source = Column(Text, nullable=True)

    # AI generated title
    title = Column(String(255), nullable=True)

    # AI generated summary
    summary = Column(Text, nullable=True)

    # Original note or fetched webpage content
    content = Column(Text, nullable=False)

    # Created timestamp
    created_at = Column(DateTime, default=datetime.utcnow)

    # One Item -> Many Chunks
    chunks = relationship(
        "Chunk",
        back_populates="item",
        cascade="all, delete-orphan"
    )