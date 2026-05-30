from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import CulturalObject


async def get_all_objects(db: AsyncSession) -> list[CulturalObject]:
    result = await db.execute(select(CulturalObject))
    return list(result.scalars().all())


async def get_object_by_id(db: AsyncSession, obj_id: int) -> CulturalObject | None:
    result = await db.execute(select(CulturalObject).where(CulturalObject.id == obj_id))
    return result.scalar_one_or_none()


async def get_object_by_name(db: AsyncSession, name: str) -> CulturalObject | None:
    result = await db.execute(select(CulturalObject).where(CulturalObject.name == name))
    return result.scalar_one_or_none()
