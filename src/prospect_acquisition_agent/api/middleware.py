from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.prospect_acquisition_agent.config.settings import get_app_settings
from src.prospect_acquisition_agent.helper.context import set_trace_id
from src.prospect_acquisition_agent.helper.id_generator import generate_id


class TraceIdMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        """
        Initialize the middleware.
        :param app: The ASGI application.
        """

        super().__init__(app)
        self.trace_id_header = get_app_settings().logging.trace_id_header

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        """
        Process the request and set trace_id from header or generate new one if not present
        :param request: The incoming HTTP request.
        :param call_next: The next middleware or endpoint to execute
        :return: the HTTP response.
        """
        trace_id = request.headers.get(self.trace_id_header)
        if not trace_id:
            trace_id = generate_id()
        set_trace_id(trace_id)
        return await call_next(request)