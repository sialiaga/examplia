from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import lesson
from .routers.telegram import telegram
from .routers.websocket import websocket_router
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.include_router(lesson.router)
app.include_router(telegram)
app.include_router(websocket_router)

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
