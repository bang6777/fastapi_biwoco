from pydantic import BaseModel
from typing import Any, Optional

class ResponseWrapper(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

    @staticmethod
    def success_response(data: Any = None, message: str = "Success"):
        return {"success": True, "message": message, "data": data}

    @staticmethod
    def error_response(message: str, data: Any = None):
        return {"success": False, "message": message, "data": data}
