from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.query import QueryRequest, QueryResponse
from app.services.query_service import query_knowledge

router = APIRouter(tags=["Query"])


@router.post(
    "/query",
    response_model=QueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask a Question"
)
def query(request: QueryRequest, db: Session = Depends(get_db)):
    return query_knowledge(db, request.question)