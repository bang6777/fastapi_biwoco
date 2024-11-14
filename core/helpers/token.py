from datetime import datetime, timedelta

import jwt

from core.config import config
from core.exceptions.custom_exception import CustomException


class DecodeTokenException(CustomException):
    def __init__(self):
        super().__init__(code=400, error_code="TOKEN__DECODE_ERROR", message="Token decode error")

class ExpiredTokenException(CustomException):
    def __init__(self):
        super().__init__(code=401, error_code="TOKEN__EXPIRE_TOKEN", message="Expired token")


class TokenHelper:
    @staticmethod
    def encode(payload: dict, expire_period: int = 3600) -> str:
        token = jwt.encode(
            {
                **payload,
                "exp": datetime.now() + timedelta(seconds=expire_period),
            },
            config.JWT_SECRET_KEY,
            config.JWT_ALGORITHM,
        )
        return token

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                config.JWT_ALGORITHM,
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredTokenException
        
    @staticmethod
    def get_user_id_from_token(token: str) -> str:
        try:
            """Extracts user ID from the JWT."""
            payload = TokenHelper.decode(token)
            user_id = payload.get("_id")
            if not user_id:
                raise CustomException(code=401, error_code="TOKEN__INVALID", message="Invalid token")
            return user_id
        except CustomException:
            raise CustomException(code=401, error_code="TOKEN__INVALID", message="Invalid token")

    @staticmethod
    def decode_expired_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                config.JWT_SECRET_KEY,
                config.JWT_ALGORITHM,
                options={"verify_exp": False},
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
