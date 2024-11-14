from fastapi import Request
from fastapi.responses import JSONResponse
from sentry_sdk import capture_exception
import json
from starlette.middleware.base import BaseHTTPMiddleware

from core.exceptions.custom_exception import CustomException
from core.helpers.response.response_wrapper import ResponseWrapper

class CustomResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            body = b"".join([section async for section in response.body_iterator])
            async def new_body_iterator():
                yield body
            response.body_iterator = new_body_iterator()  # Reset the body iterator
            try:
                data = json.loads(body.decode())
                if "openapi" not in data and "swagger" not in data and response.status_code == 200:
                    return JSONResponse(ResponseWrapper.success_response(data=data))
                else:
                    return response
            except json.JSONDecodeError:
                return response
            
        except CustomException as exc:
            # Catch and format custom exceptions
            capture_exception(exc)
            return JSONResponse(content=exc.to_response(), status_code=exc.code)
        except Exception as exc:
            capture_exception(exc)
            # Handle unexpected exceptions with a generic error message
            return JSONResponse(
                content=ResponseWrapper.error_response(message="An unexpected error occurred"),
                status_code=500
            )
