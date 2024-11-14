from app.users.application.services import UserService
from app.users.adapter.output.user_repository import UserRepository

def get_user_service() -> UserService:
    return UserService(repository=UserRepository())
