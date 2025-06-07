from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import frontend
from .routers import lesson
from .routers.telegram import telegram
from .routers.websocket import websocket_router
import os
from dotenv import load_dotenv


app = FastAPI()



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

#load_dotenv(os.path.join(CURRENT_DIR, ".env"))
#
#print("From main.py", os.getenv("PBKEY"))

app.include_router(frontend.router)
app.include_router(lesson.router)
app.include_router(telegram)
app.include_router(websocket_router)

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
