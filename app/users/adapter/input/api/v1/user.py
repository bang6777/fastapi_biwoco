from fastapi import APIRouter, Depends, Request, File, UploadFile
from sentry_sdk import capture_exception
from app.users.application.services import UserService
from app.container import Container

from dependency_injector.wiring import inject, Provide

from core.config import config
from core.fastapi.dependencies.permission import PermissionDependency, IsAuthenticated, IsAdmin
from core.helpers.s3 import S3Helper
from core.exceptions.custom_exception import CustomException
from core.db.redis.redis_client import RedisClient

from app.users.adapter.input.api.v1.request import LoginRequest, DeleteUserRequest, RegisterRequest
from app.users.adapter.input.api.v1.response import LoginResponse

user_router = APIRouter()

@user_router.get("/get-me", dependencies=[Depends(PermissionDependency([IsAuthenticated]))])
async def get_me(request: Request):
    
    user = request.state.user
    return user


@user_router.post("/register")
@inject
async def register_user(
    request: RegisterRequest, user_service: UserService = Depends(Provide[Container.user_service])
):
    return await user_service.register_user(request.email, request.password)


@user_router.post("/login", response_model=LoginResponse)
@inject
async def login_user(
    request: LoginRequest, user_service: UserService = Depends(Provide[Container.user_service])
):
    return await user_service.login_user(request.email, request.password)


@user_router.delete("/delete-user", dependencies=[Depends(PermissionDependency([IsAdmin]))],)
@inject
async def delete_user(
    request: DeleteUserRequest, user_service: UserService = Depends(Provide[Container.user_service])
):
    return await user_service.delete_user(request.user_id)


@user_router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
):
    try:
        # Read file data
        file_data = await file.read()
        s3_helper = S3Helper(aws_access_key=config.AWS_ACCESS_KEY, aws_secret_key=config.AWS_SECRET_KEY, aws_region=config.AWS_REGION)
        
        # Upload file to S3
        file_url = s3_helper.upload_file(file_data=file_data, file_name=file.filename)
        
        # Return the file URL
        return {"file_url": file_url}
    except Exception as e:
        print("Error: ", e)
        raise CustomException(code=400, error_code="FILE__UPLOAD_FAILED", message="Failed to upload image")

@user_router.get("/activate")
@inject
async def active_user(token: str, 
                      user_service: UserService = Depends(Provide[Container.user_service])):
    try:
        redis_client = RedisClient()
        
        user_id = redis_client.get_value(token)
        if not user_id:
            raise CustomException(code=400, error_code="ACTIVATE__LINK_EXPIRED", message="Activation link has expired")

        result = await user_service.active_user(str(user_id))
        redis_client.delete(token)
        return result
    
    except Exception as e:
        raise CustomException(code=400, error_code="ACTIVATE__FAILED", message="Failed to activate user")