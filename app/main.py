from fastapi import FastAPI
from app.routers import telegram, lesson

app = FastAPI()

app.include_router(lesson.router)
app.include_router(telegram.router)
