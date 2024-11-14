from core.db.mixin.timestamp_mixin import TimestampMixin


class User(TimestampMixin):
    email: str
    name: str = None
    password: str
    avatar: str = None
    is_active: bool = False
    is_admin: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "name",
                "avatar": "avatar",
                "password": "hashedpasswordstring",
                "is_active": False,
                "is_admin": False,
            }
        }
