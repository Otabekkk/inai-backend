from sqlalchemy import Column, Integer, String
from app.database.db import Base

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True, index = True, nullable = False)
    hashed_pas = Column(String, nullable = False)
