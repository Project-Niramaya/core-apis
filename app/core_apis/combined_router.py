from fastapi import FastAPI, APIRouter

from .login import router as loginRouter
from .register import router as registerRouter
from .request_utils import router as requestUtilsRouter
from .ABHA_endpoints.search import router as searchRouter


combined_router = APIRouter()   #create instance of APIRouter

#combine all the router instances into one router instance to be used in app instance

combined_router.include_router(loginRouter)
combined_router.include_router(registerRouter)
combined_router.include_router(requestUtilsRouter)
combined_router.include_router(searchRouter)

