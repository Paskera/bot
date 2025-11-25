from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from bot.config import settings
import os
from .base import Base

# SQLite
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "database.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Только для SQLite
    # echo=settings.DEBUG,  # Логируем SQL запросы в DEBUG режиме
    # pool_pre_ping=True,   # Проверяем соединение перед использованием
    # pool_recycle=3600     # Переподключаемся каждый час
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Таблицы успешно созданы!")
    except Exception as e:
        print(f"Ошибка при создание таблиц {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()