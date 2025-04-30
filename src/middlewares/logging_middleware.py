from src.middlewares.middleware import Middleware
import logging
import timeit
import sys

class LoggingMiddleware(Middleware):
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(handler)

    def preprocess_request(self, request):
        self.start = timeit.default_timer()

    def postprocess_request(self, request, status: int, headers: list, body: bytes):
        total_time = (timeit.default_timer() - self.start) * 1000
        self.logger.info(f"[INFO] {request.request_method} {request.path_info} {status} -> {total_time:.2f} ms")
        return status, body