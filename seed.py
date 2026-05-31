import asyncio

from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.models import CulturalObject

DATA = [
    {
        "name": "bolshoi_theater",
        "description": "Государственный академический Большой театр России — один " \
                       "из крупнейших и старейших театров оперы и балета в мире.",
        "address": "Театральная площадь, 1, Москва",
        "year_built": 1825,
        "architect": "Осип Бове",
        "style": "Классицизм",
        "latitude": 55.7601,
        "longitude": 37.6186,
    },
    {
        "name": "christ_spasitel",
        "description": "Храм Христа Спасителя — кафедральный собор Русской православной " \
                       "церкви, воссозданный храм-памятник.",
        "address": "ул. Волхонка, 15, Москва",
        "year_built": 2000,
        "architect": "Константин Тон",
        "style": "Русско-византийский",
        "latitude": 55.7446,
        "longitude": 37.6055,
    },
    {
        "name": "tretiakovskaya_gal",
        "description": "Государственная Третьяковская галерея — художественный музей в " \
                       "Москве, основанный купцом Павлом Третьяковым.",
        "address": "Лаврушинский переулок, 10, Москва",
        "year_built": 1856,
        "architect": "Виктор Васнецов",
        "style": "Неорусский",
        "latitude": 55.7415,
        "longitude": 37.6208,
    },
    {
        "name": "vasiliy_blazhenov",
        "description": "Храм Василия Блаженного (Покровский собор) — православный храм на " \
                       "Красной площади, памятник архитектуры XVI века.",
        "address": "Красная площадь, 7, Москва",
        "year_built": 1561,
        "architect": "Барма и Постник",
        "style": "Русское зодчество",
        "latitude": 55.7525,
        "longitude": 37.6231,
    },
    {
        "name": "visotka_kotel",
        "description": "Высотное здание на Котельнической набережной — одна из сталинских " \
                       "высоток, построенная в 1952 году.",
        "address": "Котельническая набережная, 1/15, Москва",
        "year_built": 1952,
        "architect": "Дмитрий Чечулин",
        "style": "Сталинский ампир",
        "latitude": 55.7472,
        "longitude": 37.6428,
    },
]


async def seed():
    async with SessionLocal() as db:
        for item in DATA:
            existing = await db.execute(
                select(CulturalObject).where(CulturalObject.name == item["name"])
            )
            if existing.scalar_one_or_none() is None:
                db.add(CulturalObject(**item))
        await db.commit()
        print(f"Seeded {len(DATA)} objects")


if __name__ == "__main__":
    asyncio.run(seed())
