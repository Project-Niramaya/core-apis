from fastapi import FastAPI, APIRouter

from .login import router as loginRouter
from .register import router as registerRouter
from .request_utils import router as requestUtilsRouter

combined_router = APIRouter()

combined_router.include_router(loginRouter)
combined_router.include_router(registerRouter)
combined_router.include_router(requestUtilsRouter)
