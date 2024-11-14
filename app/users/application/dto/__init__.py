from pydantic import BaseModel, Field

class LoginResponseDTO(BaseModel):
    access_token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
