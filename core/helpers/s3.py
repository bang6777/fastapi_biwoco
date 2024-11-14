import boto3
from botocore.exceptions import NoCredentialsError
from sentry_sdk import capture_exception
import uuid
import mimetypes

from core.config import config

class S3Helper:
    def __init__(self, aws_access_key: str = None, aws_secret_key: str = None, aws_region: str = None):
        access_key = aws_access_key or config.AWS_ACCESS_KEY
        secret_key = aws_secret_key or config.AWS_SECRET_KEY
        region = aws_region or config.AWS_REGION

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )

    def upload_file(self, file_data: bytes, file_name: str, folder: str = "uploads") -> str:
        unique_file_name = f"{folder}/{uuid.uuid4()}_{file_name}"
        content_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"

        try:
            self.s3_client.put_object(
                Bucket=config.AWS_S3_BUCKET,
                Key=unique_file_name,
                Body=file_data,
                ContentType=content_type,
            )
            return f"{config.AWS_S3_URL}{unique_file_name}"
        except NoCredentialsError as e:
            capture_exception(e)
            raise Exception("AWS credentials not found.")
