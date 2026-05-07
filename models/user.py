from pydantic import BaseModel, EmailStr
from typing import Literal

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: Literal["admin", "agent_assurance"]

class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    full_name: str