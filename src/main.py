from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.controllers import account, auth, transaction
from src.database import database
from src.exceptions import AccountNotFoundError, BusinessError

# --- Rate Limiter ---
limiter = Limiter(key_func=get_remote_address, default_limits=["100 per minute"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


tags_metadata = [
    {
        "name": "auth",
        "description": "Operations for authentication.",
    },
    {
        "name": "account",
        "description": "Operations to maintain accounts.",
    },
    {
        "name": "transaction",
        "description": "Operations to maintain transactions.",
    },
]


app = FastAPI(
    title="Transactions API",
    version="1.0.0",
    summary="Microservice to maintain withdrawal and deposit operations from current accounts.",
    description="""
Transactions API is the microservice for recording current account transactions. 💸💰

## Account

* **Create accounts**.
* **List accounts**.
* **List account transactions by ID**.

## Transaction

* **Create transactions**.
""",
    openapi_tags=tags_metadata,
    redoc_url=None,
    lifespan=lifespan,
)

# --- Middlewares ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
# Aplicando um limite mais estrito para o endpoint de autenticação
app.include_router(auth.router, prefix="/auth", tags=["auth"])
@app.post("/auth/token")
@limiter.limit("5 per minute")
async def limited_auth_token(request: Request):
    return await auth.login_for_access_token(request)

app.include_router(account.router, prefix="/accounts", tags=["account"])
app.include_router(transaction.router, prefix="/transactions", tags=["transaction"])


# --- Exception Handlers ---
@app.exception_handler(AccountNotFoundError)
async def account_not_found_error_handler(request: Request, exc: AccountNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Account not found."})


@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError):
    return JSONResponse(status_code=status.HTTP_450_CONFLICT, content={"detail": str(exc)})
