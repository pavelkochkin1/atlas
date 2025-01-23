from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GIGA_KEY: str
    NEO4J_URL: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str


load_dotenv(dotenv_path="./.env", verbose=True)
settings = Settings()
