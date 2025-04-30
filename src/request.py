from urllib.parse import parse_qs
import json

class Request:
    def __init__(self, environ: dict):
        for key, value in environ.items():
            setattr(self, key.replace('.', '_').lower(), value)

        self.casted_params = {}
        self.url_params = {}
        self.body_params = {}

        for key, values_list in parse_qs(self.query_string).items():
            self.url_params[key] = values_list[-1] 

        request_body_size = int(getattr(self, 'content_length', 0))
        if request_body_size > 0:
            request_body = self.wsgi_input.read(request_body_size)
            body_params = json.loads(request_body.decode())
            if isinstance(body_params, dict):
                self.body_params = body_params