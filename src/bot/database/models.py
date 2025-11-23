from sqlalchemy import Column, Integer, String, Boolean, JSON, Text
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    vk_id  = Column(Integer)
    name = Column(Text)
    test1 = Column(Boolean)
    test2 = Column(Boolean)
    test3 = Column(Boolean)


