from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.models.chunk import Chunk
from app.models.item import Item
from app.routes.item import router as item_router
from app.routes.query import router as query_router

app = FastAPI(
    title="AI Knowledge Inbox",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# -----------------------------
# CORS Configuration
# -----------------------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Allow React frontend
    allow_credentials=True,
    allow_methods=["*"],        # Allow all HTTP methods
    allow_headers=["*"],        # Allow all headers
)

# -----------------------------
# Register Routes
# -----------------------------
app.include_router(item_router)
app.include_router(query_router)

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def root():
    return {
        "message": "AI Knowledge Inbox Backend Running"
    }