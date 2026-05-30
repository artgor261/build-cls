from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User
from app.core.schemas import UserCreate


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: UserCreate, hashed_password: str) -> User:
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        name=user.name,
        surname=user.surname,
        city=user.city,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
