from sqlalchemy import Column, Integer, String, Text
from app.database.db import Base

class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable = False)
    description = Column(Text, nullable = False)
