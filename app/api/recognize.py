import pickle

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.object import get_object_by_class_name
from app.core.database import get_db
from app.core.schemas import RecognizeResponse
from app.services.classifier import predict
from app.services.images import to_response

router = APIRouter(prefix="/recognize", tags=["recognize"])

with open(settings.ENCODER_PATH, "rb") as f:
    label_encoder = pickle.load(f)


@router.post("", response_model=RecognizeResponse)
async def recognize(file: UploadFile, db: AsyncSession = Depends(get_db)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be an image")

    try:
        image = Image.open(file.file).convert("RGB")
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file")

    class_id = predict(image)
    class_name = label_encoder.inverse_transform([class_id])[0]
    obj = await get_object_by_class_name(db, class_name)

    return RecognizeResponse(
        class_name=class_name,
        object=to_response(obj) if obj else None,
    )
