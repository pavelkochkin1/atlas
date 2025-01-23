from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    NEO4J_HOST: str
    NEO4j_PORT: int
    NEO4J_USER: str
    NEO4J_PASSWORD: str


load_dotenv(dotenv_path="./.env", verbose=True)
settings = Settings()
