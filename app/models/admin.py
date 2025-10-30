from sqlalchemy import Column, Integer, String, Boolean
from app.database.db import Base

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True, index = True, nullable = False)
    hashed_pas = Column(String, nullable = False)
    is_admin = Column(Boolean, default=True)