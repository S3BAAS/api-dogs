from fastapi import FastAPI, Request
from app.routers import crud
from app.middleware.rate_limit import rate_limit_middleware

app = FastAPI()


# --- MIDDLEWARE ---
@app.middleware("http")
async def add_rate_limit_header(request: Request, call_next):
    return await rate_limit_middleware(request, call_next)

# --- ROUTERS ---
app.include_router(crud.router)
