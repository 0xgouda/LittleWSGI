
class Middleware():
    def preprocess_request(self, request):
        return

    def postprocess_request(self, request, status: int, headers: list, body: bytes):
        return status, body