from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from enum import Enum

#----------------------
# User
#----------------------
class UserBase(BaseModel):
    username: str
    password: str

    @field_validator('username')
    @classmethod
    def username_not_empty(cls, v):
        if not v or len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v

    @field_validator('password')
    @classmethod
    def password_strong_enough(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v


# ----------------------
# User Signup / Login
# ----------------------
class UserSignup(UserBase):
    """To create an account."""
    pass


class UserLogin(UserBase):
    """Login details."""
    pass


# ----------------------
# User Response
# ----------------------
class UserResponse(BaseModel):
    """User returned after signup/login (no password!)"""
    id: int
    username: str

    model_config = {"from_attributes": True}


# ----------------------
# Token
# ----------------------
class TokenOut(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"

#----------------------
# Game
#----------------------

#----------------------
# Move
#----------------------