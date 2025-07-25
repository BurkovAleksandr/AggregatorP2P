from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# замените URL вашей БД
DB_URL = "postgresql+psycopg2://aggregator:securepassword@localhost:5432/aggregatorp2p"

# создаём движок
engine = create_engine(DB_URL, echo=True, future=True)

# фабрика сессий
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
