from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Password")

class IdRequest(BaseModel):
    user_id: str = Field(..., description="User ID")