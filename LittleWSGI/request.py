class Request:
    def __init__(self, environ: dict):
        for key, value in environ.items():
            setattr(self, key.replace('-', '_').lower(), value)