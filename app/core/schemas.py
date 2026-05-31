from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    name: str = ""
    surname: str = ""
    city: str = ""


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    name: str = ""
    surname: str = ""
    city: str = ""

    model_config = {"from_attributes": True}


class ObjectResponse(BaseModel):
    id: int
    name: str
    description: str = ""
    address: str = ""
    year_built: int | None = None
    architect: str = ""
    style: str = ""
    latitude: float | None = None
    longitude: float | None = None

    model_config = {"from_attributes": True}


class RecognizeResponse(BaseModel):
    class_name: str
    object: ObjectResponse | None = None
