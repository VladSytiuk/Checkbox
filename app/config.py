import os

from dotenv import load_dotenv


def get_dotenv():
    if os.environ.get("environment_type") == "test":
        load_dotenv(dotenv_path=".env.test")
    load_dotenv(dotenv_path=".env")


get_dotenv()


class Config:
    # Postgres
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    # App
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    ALLOWED_PAYMENT_TYPE = ("cash", "cashless")
    DEFAULT_MAX_ROW_LENGTH = 40


settings = Config()
