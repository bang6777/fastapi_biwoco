from pydantic import BaseModel, Field


class LoginResponse(BaseModel):
    access_token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")