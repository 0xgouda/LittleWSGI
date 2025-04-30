from src.request import Request
from src.router import Router, SUPPORTED_HTTP_METHODS
from inspect import Parameter
from http import HTTPMethod, HTTPStatus
from src.exceptions import HTTPException
from src.response import Response

class LittleWSGI():

    def __init__(self, router: Router):
        self.router = router
        self.middlewares = []
    
    def __call__(self, environ, start_response):
        try:
            request = Request(environ)
            
            for middleware in self.middlewares:
                middleware.preprocess_request(request) 

            method, handler, function_params = self.router.routes.get(request.path_info)
            if method != request.request_method:
                raise HTTPException(HTTPStatus.METHOD_NOT_ALLOWED)

            if method == HTTPMethod.GET:
                request_params = request.url_params
            elif method in SUPPORTED_HTTP_METHODS:
                request_params = request.body_params

            for param_name, param in function_params.items():
                if param.default is not Parameter.empty:
                    request.casted_params[param_name] = param.default

                if param_name in function_params:    
                    try:
                        request.casted_params[param_name] = param.annotation(request_params[param_name])
                    except (ValueError, KeyError):
                        raise HTTPException(HTTPStatus.BAD_REQUEST)

                if param_name not in request.casted_params:
                    raise HTTPException(HTTPStatus.BAD_REQUEST)

                    
            status, headers, body = handler(**request.casted_params)
            
            for middleware in self.middlewares:
                status, body = middleware.postprocess_request(request, status, headers, body)
            
            start_response(status, headers)
            return body

        except HTTPException as e:
            status, headers, body = Response(e.getMessage(), e.getHTTPStatus()).response()
            start_response(status, headers)
            return body

        #except Exception as e:
            #status, headers, body = Response("Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR).response()
            #start_response(status, headers)
            #return body

    def add_middleware(self, middleware):
        if middleware not in self.middlewares:
            self.middlewares.append(middleware)