from sqlalchemy import Column, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(255), default="", nullable=False)
    surname = Column(String(255), default="", nullable=False)
    city = Column(String(255), default="", nullable=False)


class CulturalObject(Base):
    __tablename__ = "cultural_objects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, default="")
    address = Column(String(255), default="")
    year_built = Column(Integer, nullable=True)
    architect = Column(String(255), default="")
    style = Column(String(255), default="")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
