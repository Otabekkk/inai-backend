from pydantic import BaseModel, EmailStr, Field

class AdminBase(BaseModel):
    email: EmailStr

class AdminCreate(AdminBase):
    password: str = Field(..., min_length=8, max_length=72, description="Password must be 8-72 characters")

class AdminLogin(AdminBase):
    password: str = Field(..., min_length=8, max_length=72, description="Password must be 8-72 characters")

class AdminOut(AdminBase):
    id: int

    class Config:
        from_attributes = True
        