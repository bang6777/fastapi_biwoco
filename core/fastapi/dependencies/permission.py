from abc import ABC, abstractmethod
from typing import Type
from sentry_sdk import capture_exception

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from starlette import status

from app.container import Container
from app.users.application.services import UserService
from core.exceptions.custom_exception import CustomException
from core.helpers.token import TokenHelper
from core.fastapi.dependencies.dependencies import get_user_service


class UnauthorizedException(CustomException):
    code = status.HTTP_401_UNAUTHORIZED
    error_code = "UNAUTHORIZED"
    message = ""

class ForbiddenException(CustomException):
    code = status.HTTP_403_FORBIDDEN
    error_code = "FORBIDDEN"
    message = "You don't have permission to access this resource"


class BasePermission(ABC):
    exception = CustomException

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        """has permssion"""


class IsAuthenticated(BasePermission):

    @inject
    async def has_permission(self, request: Request) -> bool:
        try:
            token = request.headers.get("Authorization")
            user_service: UserService = get_user_service()
            user = await user_service.get_current_user(token)
            if not user:
                raise self.exception
            request.state.user = user
            return True
        except Exception as e:
            capture_exception(e)
            raise CustomException(code=401, error_code="UNAUTHORIZED", message="Failed to authenticate user")

class IsAdmin(BasePermission):
    @inject
    async def has_permission(
        self,
        request: Request
    ) -> bool:
        try:
            token = request.headers.get("Authorization")
            user_service: UserService = get_user_service()
            # user_id = TokenHelper.get_user_id_from_token(token)
            is_admin = await user_service.is_admin(token)
            if not is_admin:
                raise 
            return is_admin
        except Exception as e:
            capture_exception(e)
            raise CustomException(code=403, error_code="FORBIDDEN", message="Failed to check if user is admin")

class AllowAll(BasePermission):
    async def has_permission(self, request: Request) -> bool:
        return True


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: list[Type[BasePermission]]):
        self.permissions = permissions
        self.model: APIKey = APIKey(
            **{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request):
        for permission in self.permissions:
            cls = permission()
            if not await cls.has_permission(request=request):
                raise cls.exception
