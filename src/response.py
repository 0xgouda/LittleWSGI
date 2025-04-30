from http import HTTPStatus
import json

SUPPORTED_RESPONSE_CONTENT_TYPES = ["application/json"]

class Response:
    def __init__(self, body, status: HTTPStatus | None = None, content_type: str = "application/json"):
        self.body = body
        status = status or HTTPStatus.OK
        self.status = f"{status.value} {status.phrase}"
        self.content_type = content_type

    def as_iter_of_bytes(self):
        if self.content_type not in SUPPORTED_RESPONSE_CONTENT_TYPES:
            raise ValueError("unsupported response Content-Type") 

        body_bytes = json.dumps(self.body).encode()
        return [body_bytes]

    def response(self):
        iter = self.as_iter_of_bytes()
        length = sum(len(b) for b in iter)

        headers = [
            ("Content-Type", self.content_type),
            ("Content-Length", str(length))
        ]
        
        return self.status, headers, iter
