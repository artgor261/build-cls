import base64
from pathlib import Path

from app.core.models import CulturalObject
from app.core.schemas import ObjectResponse


def _image_to_base64(path: str) -> str | None:
    full_path = Path(path.lstrip("/"))
    if not full_path.exists():
        return None
    with open(full_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def to_response(obj: CulturalObject) -> ObjectResponse:
    return ObjectResponse(
        id=obj.id,
        name=obj.name,
        description=obj.description or "",
        address=obj.address or "",
        year_built=obj.year_built,
        architect=obj.architect or "",
        style=obj.style or "",
        latitude=obj.latitude,
        longitude=obj.longitude,
        image_base64=_image_to_base64(obj.image_url) if obj.image_url else None,
    )
