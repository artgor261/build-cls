from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.object import get_all_objects, get_object_by_id
from app.core.database import get_db
from app.core.schemas import ObjectResponse
from app.services.images import to_response

router = APIRouter(prefix="/objects", tags=["objects"])


@router.get("", response_model=list[ObjectResponse])
async def objects(db: AsyncSession = Depends(get_db)):
    return [to_response(obj) for obj in await get_all_objects(db)]


@router.get("/{obj_id}", response_model=ObjectResponse)
async def object_by_id(obj_id: int, db: AsyncSession = Depends(get_db)):
    obj = await get_object_by_id(db, obj_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
    return to_response(obj)
