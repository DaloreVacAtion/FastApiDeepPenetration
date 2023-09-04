from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.router import root_router
from core import settings
from core.logging import logger

app = FastAPI(
    debug=settings.DEBUG
)

app.logger = logger

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=root_router)

