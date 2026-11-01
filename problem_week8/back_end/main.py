import time

from fastapi import Cookie, FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    print(f"{request.method} {request.url.path} -> "
          f"{response.status_code} ({time.perf_counter() - start:.3f}s)")
    return response


@app.get("/visits")
def count_visits(response: Response, visits: str | None = Cookie(default=None)):
    count = int(visits) if visits else 0
    count += 1
    response.set_cookie(key="visits", value=str(count),
                        httponly=True, samesite="lax")
    return {"visits": count}


app.mount("/", StaticFiles(directory="../front_end", html=True), name="static")
