from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/buildings"
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    MODEL_PATH: str = "app/model/classifier.pt"
    ENCODER_PATH: str = "app/model/label_encoder.pkl"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
