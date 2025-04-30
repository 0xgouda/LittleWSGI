# LittleWsgi

- Just a little Python framework for exploring WSGI

### example usage

```python
from src.router import Router
from src.app import LittleWSGI
from src.middlewares.logging_middleware import LoggingMiddleware
from http import HTTPMethod

router = Router()
@router.route(HTTPMethod.POST, '/greet')
def fun(x: str):
    return f"Hello, {x}"

data = [1, 2, 3, 4]
@router.route(HTTPMethod.GET, '/data')
def fun2() -> list:
    return data

app = LittleWSGI(router=router)
app.add_middleware(LoggingMiddleware())
```

### running

```bash
gunicorn example:app -b :8888
...
[INFO] GET /data 200 OK -> 0.05 ms
```