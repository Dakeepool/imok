from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

# Base User schema
class UserBase(BaseModel):
    username: str
    email: EmailStr

# User creation schema (for registration)
class UserCreate(UserBase):
    password: str
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

# User response schema (without sensitive data)
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# User login schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token schema for response
class Token(BaseModel):
    access_token: str
    token_type: str

# Token data schema for internal use
class TokenData(BaseModel):
    email: Optional[str] = None
