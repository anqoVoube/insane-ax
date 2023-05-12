import logging

from starlette.requests import Request
from starlette.responses import Response


class LoggingMiddleware:
    def __init__(self, request: Request, response: Response):
        self.request = request
        self.response = response

    def launch_logging(self):
        self.logger(
            self.create_log_string(
                self.http_method,
                self.url_path,
                self.client_host,
                self.status_code
            )
        )

    @property
    def logger(self):
        if self.response.status_code // 100 == 5:
            # Status code is 500 <= status_code < 600
            return getattr(logging, "error")
        return getattr(logging, "info")

    @property
    def http_method(self) -> str:
        return self.request.method

    @property
    def url_path(self) -> str:
        return self.request.url.path

    @property
    def client_host(self) -> str:
        return self.request.client.host

    @property
    def status_code(self) -> int:
        return self.response.status_code

    @staticmethod
    def create_log_string(*args, join_with: str = " - "):
        return join_with.join(map(str, args))
