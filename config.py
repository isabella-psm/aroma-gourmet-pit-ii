import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Config:
    # No Render, defina SECRET_KEY como variavel de ambiente.
    SECRET_KEY = os.getenv("SECRET_KEY", "desenvolvimento-local-apenas")
    DATABASE = BASE_DIR / "instance" / "cafeteria.db"
    # Defina DATABASE_URL para usar PostgreSQL, por exemplo:
    # postgresql://aroma:aroma@localhost:5432/aroma_gourmet
    DATABASE_URL = os.getenv("DATABASE_URL")
