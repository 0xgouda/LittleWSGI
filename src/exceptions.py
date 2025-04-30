from http import HTTPStatus

class HTTPException(Exception):
    def __init__(self, status: HTTPStatus):
        self.status = status
        self.message = status.phrase
        super().__init__(self.message) 

    def getHTTPStatus(self):
        return self.status

    def getMessage(self):
        return self.message