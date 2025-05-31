from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import telegram, lesson
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.include_router(lesson.router)
app.include_router(telegram.router)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
