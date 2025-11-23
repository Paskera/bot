import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    vk_id  = Column(Integer, nullable=False)
    name = Column(Text)
    test_id = Column(Integer, nullable=True)