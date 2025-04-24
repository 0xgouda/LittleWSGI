from request import Request
from router import Router

class LittleWSGI():

    def __init__(self, router: Router):
        self.router = router
    
    def __call__(self, environ, start_response):
        request = Request(environ)
        
        method, handler = self.router.routes.get(request.path_info)
        status, headers, body = handler()
        
        start_response(status, headers)
        return body