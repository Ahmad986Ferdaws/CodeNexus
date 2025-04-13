from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    
    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'Username must be alphanumeric'
        return v


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Properties to return via API
class User(UserInDBBase):
    pass


# Properties stored in DB, not returned by API
class UserInDB(UserInDBBase):
    hashed_password: str
