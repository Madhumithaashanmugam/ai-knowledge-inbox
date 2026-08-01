from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    chunk_text = Column(Text, nullable=False)

    # Store embedding as JSON string
    embedding = Column(Text, nullable=True)

    item = relationship("Item", back_populates="chunks")