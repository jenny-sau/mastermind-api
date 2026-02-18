from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de connexion PostgreSQL
DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/mastermind"

# Moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()

# Dépendance FastAPI pour injecter la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()