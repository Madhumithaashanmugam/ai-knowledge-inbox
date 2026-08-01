from typing import List

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.item import ItemCreate, ItemResponse
from app.services.item_service import create_item, get_items

router = APIRouter(tags=["Items"])


@router.post(
    "/ingest",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Note or URL"
)
def ingest_item(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)


@router.get(
    "/items",
    response_model=List[ItemResponse],
    status_code=status.HTTP_200_OK,
    summary="Get All Items"
)
def list_items(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(9, ge=1, le=50, description="Items per page"),
    db: Session = Depends(get_db)
):
    return get_items(
        db=db,
        page=page,
        limit=limit
    )