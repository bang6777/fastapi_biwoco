from passlib.context import CryptContext
from sentry_sdk import capture_exception
import uuid

from core.config import config
from core.helpers.token import TokenHelper
from core.exceptions.custom_exception import CustomException
from core.helpers.emails.email import EmailHelper
from core.db.redis.redis_client import RedisClient

from app.users.domain.entity.user import User

from app.users.application.dto import LoginResponseDTO
from app.users.adapter.output.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, repository: UserRepository):
        self.repo = repository
        self.email_helper = EmailHelper()

    async def get_current_user(self, token: str) -> User:
        try:
            user_id = TokenHelper.get_user_id_from_token(token)
            user = await self.repo.find_by_id(user_id)
            if not user:
                raise CustomException(code=404, error_code="USER__NOT_FOUND", message="User not found")

            return user
        except CustomException:
            raise
        except Exception as e:
            capture_exception(e)
            raise CustomException(code=500, error_code="USER__EXCEPTION", message="Failed to retrieve current user")

        
    async def is_admin(self, token: str) -> bool:
        try:
            user_id = TokenHelper.get_user_id_from_token(token)
            user = await self.repo.find_by_id(user_id)
            if not user:
                return False

            if not user['is_admin']:
                return False

            return True
        except CustomException:
            raise
        except Exception as e:
            capture_exception(e)
            raise CustomException(code=500, message="Failed to check if user is admin")

    
    async def delete_user(self, user_id: str):
        user = await self.repo.find_by_id(user_id)
        if not user:
            raise CustomException(code=404, error_code="USER__NOT_FOUND", message="User not found")
        await self.repo.delete_user(user_id)
        return {}

    async def register_user(self, email: str, password: str) -> dict:
        hashed_password = pwd_context.hash(password)
        existing_user = await self.repo.find_by_email(email)
        if existing_user:
            raise CustomException(
                code=400, error_code="USER__ALREADY_EXISTS", message="User already exists")
        new_user = User(email=email, password=hashed_password)
        data = await self.repo.create_user(new_user.model_dump())
        await self.send_activation_email(data)
        return data
    
    async def send_activation_email(self, user: User):
        # Generate activation token with expiration time, e.g., 24 hours
        try:
            activation_token = str(uuid.uuid4())
            redis_client = RedisClient()
            redis_client.set(activation_token, str(user.get("_id")), 600)

            # Construct the activation link
            activation_link = f"http://{config.APP_HOST}:{config.APP_PORT}/api/v1/user/activate?token={activation_token}"

            # Send the email
            subject = "Welcome to Biwoco test!"
            template_name = "active_email.html"

            context = {
                "email": user.get("email"),
                "activation_link": activation_link,
            }
            await self.email_helper.send_email_with_template(
                to_email=user.get("email"),
                subject=subject,
                template_name=template_name,
                context=context
            )
        except Exception as e:
            raise CustomException(code=400, error_code="EMAIL__SEND_FAILED", message="Failed to send activation email")

    async def login_user(self, email: str, password: str) -> LoginResponseDTO:
        user = await self.repo.find_by_email(email)
        if not user or not pwd_context.verify(password, user["password"]) or not user["is_active"]:
            raise CustomException(
                code=401, error_code="AUTH__INVALID_CREDENTIALS", message="Invalid credentials")

        response = LoginResponseDTO(
            access_token=TokenHelper.encode(
                payload={"sub": user["email"], "_id": str(user["_id"])}, expire_period=config.ACCESS_TOKEN_EXPIRE_MINUTES * 60),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
        return response

    async def active_user(self, user_id: str) -> User:
        user = await self.repo.find_by_id(user_id)
        if not user:
            raise CustomException(
                code=401, error_code="USER__NOT_FOUND", message="User not found"
            )
        custom_data = {
            "is_active": True
        }
        update_user = await self.repo.update_user(user_id, custom_data)
        return update_user
