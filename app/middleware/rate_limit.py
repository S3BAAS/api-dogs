import time
from typing import Dict, Callable

from fastapi import Request, HTTPException, Response
from fastapi.responses import JSONResponse


request_times: Dict[str, list] = {}
MAX_REQUEST_TIME = 50
ENTRY_EXPIRATION_TIME = 30


async def rate_limit_middleware(request: Request, call_next: Callable[[Request], Response]):
    global request_times

    client_ip = request.client.host
    now = time.time()

    # Limpiar keys expiradas
    expired_keys = [k for k, v in request_times.items(
    ) if now - v[0] > ENTRY_EXPIRATION_TIME]
    for key in expired_keys:
        del request_times[key]

    # Verificar límite de peticiones
    if client_ip in request_times and len(request_times[client_ip]) > MAX_REQUEST_TIME:
        raise HTTPException(status_code=429, detail="Too many requests")

    # Almacenar tiempo actual
    if client_ip not in request_times:
        request_times[client_ip] = []
    request_times[client_ip].append(now)

    # Llamar al siguiente middleware o endpoint
    response = await call_next(request)

    # Calcular tiempo de procesamiento
    process_time = time.time() - now

    if isinstance(response, JSONResponse):
        response.headers["X-Process-Time"] = str(process_time)

    return response
