from request import Request
from router import Router, SUPPORTED_HTTP_METHODS
from inspect import Parameter
from http import HTTPMethod, HTTPStatus
from exceptions import HTTPException
from response import Response

class LittleWSGI():

    def __init__(self, router: Router):
        self.router = router
        self.middlewares = []
    
    def __call__(self, environ, start_response):
        try:
            request = Request(environ)
            
            method, handler, params = self.router.routes.get(request.path_info)
            for param_name, param in params.items():
                if param.default is not Parameter.empty:
                    request.casted_params[param_name] = param.default

                if param_name in request.url_params:    
                    try:
                        request.casted_params[param_name] = param.annotation(request.url_params[param_name])
                    except ValueError:
                        raise HTTPException(HTTPStatus.BAD_REQUEST)

                if param_name not in request.casted_params:
                    raise HTTPException(HTTPStatus.BAD_REQUEST)

                    
            status, headers, body = handler(**request.casted_params)
            
            start_response(status, headers)
            return body

        except HTTPException as e:
            status, headers, body = Response(e.getMessage(), e.getHTTPStatus()).response()
            start_response(status, headers)
            return body

        except Exception as e:
            status, header, body = Response("Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR).response()
            start_response(status, headers)
            return body