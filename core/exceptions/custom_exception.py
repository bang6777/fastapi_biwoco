from fastapi import HTTPException
from sentry_sdk import capture_exception
from core.helpers.response.response_wrapper import ResponseWrapper

class CustomException(HTTPException):
    def __init__(self, code: int, error_code: str, message: str):
        self.code = code
        self.error_code = error_code
        self.message = message
        capture_exception(self)
        super().__init__(status_code=code, detail=message)

    def to_response(self):
        return ResponseWrapper.error_response(
            message=self.message,
            data={"error_code": self.error_code}
        )
