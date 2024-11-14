from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton
from app.users.application.services import UserService
from app.users.adapter.output.user_repository import UserRepository

class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=["app.users.adapter.input.api.v1.user"])
    user_repository = Singleton(UserRepository)
    user_service = Factory(UserService, repository=user_repository)
