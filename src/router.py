from response import Response
from http import HTTPStatus, HTTPMethod
from inspect import signature

SUPPORTED_HTTP_METHODS = [HTTPMethod.GET, HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.DELETE, HTTPMethod.PATCH]

class Router:
    def __init__(self):
        self.routes = {}

    def route(self, method: str, path: str, status: HTTPStatus | None = None, content_type: str = "application/json"):
        method = method.upper()
        status = status or HTTPStatus.OK

        if method not in SUPPORTED_HTTP_METHODS:
            raise ValueError("Invalid HTTP Method")

        def wrapper(old_func):
            def new_func(*args, **kwds):
                body = old_func(*args, **kwds)
                return Response(body, status, content_type).response()

            self.routes[path] = (method, new_func, signature(old_func).parameters)
            return new_func

        return wrapper
