import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core import database
from core.config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(config.FILES_DIR, exist_ok=True)
    os.makedirs(config.IMAGES_DIR, exist_ok=True)
    await database.init_models()
    yield
    await database.drop_models()
