from pydantic import BaseModel, Field
from fastapi import UploadFile

class RegisterRequest(BaseModel):
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Password")
    # add more fields here

class LoginRequest(BaseModel):
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Password")

class DeleteUserRequest(BaseModel):
    user_id: str = Field(..., description="User ID")