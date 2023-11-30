from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.core_apis.combined_router import combined_router

import uvicorn


app = FastAPI()

# CORS middleware configuration
origins = [
    "http://localhost:8000",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(combined_router)

if(__name__ == "__main__"):
    uvicorn.run(app, host="127.0.0.1", port=8000)
