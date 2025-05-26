import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logging.info(f"Request: {request.method} {request.url.path}")
        try:
            response = await call_next(request)
            # Read response body for logging
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            logging.info(
                f"Response: {request.method} {request.url.path} "
                f"Status: {response.status_code} "
                f"Body: {response_body.decode('utf-8', errors='replace')}"
            )
            return Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )
        except Exception as e:
            logging.error(f"Error handling request: {e}")
            raise 