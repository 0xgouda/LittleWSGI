from request import Request
from router import Router, SUPPORTED_HTTP_METHODS
from inspect import Parameter
from http import HTTPMethod

class LittleWSGI():

    def __init__(self, router: Router):
        self.router = router
    
    def __call__(self, environ, start_response):
        request = Request(environ)
        
        method, handler, params = self.router.routes.get(request.path_info)
        for param_name, param in params.items():
            if param.default is not Parameter.empty:
                request.casted_params[param_name] = param.default
            if param_name in request.url_params:    
                request.casted_params[param_name] = param.annotation(request.url_params[param_name][-1])
        
                
        status, headers, body = handler(**request.casted_params)

        start_response(status, headers)
        return body