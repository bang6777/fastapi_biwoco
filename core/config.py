import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = os.getenv("APP_HOST", "localhost")
    APP_PORT: int = os.getenv("APP_PORT", "8000")
    # database
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DATABASE: str = os.getenv("MONGO_DATABASE", "biwoco_test")
    # aws
    AWS_S3_BUCKET: str = os.getenv("AWS_S3_BUCKET", "AWS_S3_BUCKET")
    AWS_S3_URL: str = f"https://{AWS_S3_BUCKET}.s3.amazonaws.com/"
    AWS_ACCESS_KEY: str = os.getenv("AWS_ACCESS_KEY_ID", "AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = os.getenv("AWS_REGION", "AWS_REGION")
    # jwt
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # sentry
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "SENTRY_DSN")
    # celery    
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_BACKEND_URL: str = "redis://localhost:6379/1"
    # redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379 
    REDIS_DB: int = 0
    # Email config
    MAIL_USERNAME: str = os.getenv("MAIL_CONTACT", "MAIL_CONTACT")
    MAIL_PASSWORD: str = "nvpt zczk gnej idve"
    MAIL_FROM: str = os.getenv("MAIL_CONTACT", "MAIL_CONTACT")
    MAIL_FROM_NAME: str = "Biwoco Test"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"  # SMTP server, e.g., "smtp.gmail.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    MAIL_USE_CREDENTIALS: bool = True
    MAIL_TEMPLATE_FOLDER: str = "core/helpers/templates/emails"  
    # active account token in minutes
    # ACTIVE_ACCOUNT_TOKEN_MINUTES=120
    

class LocalConfig(Config):
    ...


class ProductionConfig(Config):
    DEBUG: bool = False


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
