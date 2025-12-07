from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class NewsBase(BaseModel):
    title: str
    content: str
    
class NewsCreate(NewsBase):
    pass

class NewsOut(NewsBase):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    class Config:
        from_attributes = True
        