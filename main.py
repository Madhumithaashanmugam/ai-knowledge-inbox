import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.models.chunk import Chunk
from app.models.item import Item
from app.routes.item import router as item_router
from app.routes.query import router as query_router

# -----------------------------
# Logging Configuration
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Knowledge Inbox",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

logger.info("Database tables initialized successfully.")

# -----------------------------
# CORS Configuration
# -----------------------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("CORS middleware configured.")

# -----------------------------
# Register Routes
# -----------------------------
app.include_router(item_router)
app.include_router(query_router)

logger.info("Application routes registered successfully.")

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def root():
    logger.info("Root endpoint accessed.")

    return {
        "message": "AI Knowledge Inbox Backend Running"
    }