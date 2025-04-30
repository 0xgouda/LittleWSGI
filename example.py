from src.router import Router
from src.app import LittleWSGI
from src.middlewares.logging_middleware import LoggingMiddleware
from http import HTTPMethod

router = Router()
@router.route(HTTPMethod.POST, '/greet')
def fun(x: str):
    return f"Hello, {x}"

app = LittleWSGI(router=router)
app.add_middleware(LoggingMiddleware())