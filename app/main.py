import os

from fastapi import FastAPI

from app.config import config
from app.routers import pdf, status

app = FastAPI()
app.state.config = config

app.include_router(pdf.router)
app.include_router(status.router)

try:
    os.mkdir(f"{config.BASE_DIR}/downloads")
except FileExistsError:
    pass