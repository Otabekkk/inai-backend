from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from app.database.db import Base
import datetime

class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable = False)
    content = Column(Text, nullable = False)
    image_url = Column(String, nullable = True)
    published = Column(Boolean, default = False)
    created_at = Column(DateTime, default = datetime.datetime.utcnow)