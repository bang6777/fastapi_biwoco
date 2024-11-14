from pathlib import Path
from jinja2 import Template
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from core.config import config
from typing import Dict
from core.exceptions.custom_exception import CustomException


class EmailServiceException(CustomException):
    code = 500
    error_code = "EMAIL_SERVICE_ERROR"
    message = "Failed to send email"


conf = ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,  # Sử dụng mật khẩu ứng dụng
    MAIL_FROM=config.MAIL_FROM,
    MAIL_PORT=config.MAIL_PORT,  # Cổng SMTP TLS
    MAIL_SERVER=config.MAIL_SERVER,
    USE_CREDENTIALS=config.MAIL_USE_CREDENTIALS,
    MAIL_FROM_NAME=config.MAIL_FROM_NAME,
    MAIL_STARTTLS=config.MAIL_STARTTLS,
    MAIL_SSL_TLS=config.MAIL_SSL_TLS
)


class EmailHelper:
    def __init__(self):
        self.fast_mail = FastMail(conf)
        
    def load_template(self, template_name: str) -> str:
        """Load an HTML template as a string."""
        template_path = Path(f"core/helpers/templates/emails/{template_name}")
        try:
            return template_path.read_text()
        except FileNotFoundError:
            raise Exception(f"Template not found: {template_name}")


    async def send_email_with_template(
        self, to_email: str, subject: str, template_name: str, context: Dict[str, str]
    ):
        template_content = self.load_template(template_name)
        template = Template(template_content)
        html_content = template.render(email=context.get("email"), activation_link=context.get("activation_link"))

        message = MessageSchema(
            subject=subject,
            recipients=[to_email],
            template_body=html_content,
            subtype="html"
        )
        try:
            await self.fast_mail.send_message(message, template_name=template_name)
        except Exception as e:
            raise EmailServiceException from e
