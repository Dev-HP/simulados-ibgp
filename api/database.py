from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Usa DATABASE_URL se disponível (Supabase/PostgreSQL), senão SQLite
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback para SQLite local
    db_path = os.getenv("DATABASE_PATH", "./simulados.db")
    db_dir = os.path.dirname(db_path)
    if db_dir:
        try:
            os.makedirs(db_dir, exist_ok=True)
        except PermissionError:
            # Se não conseguir criar, usa diretório atual
            db_path = "./simulados.db"
    DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
