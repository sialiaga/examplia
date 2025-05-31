from fastapi import FastAPI
from .routers.telegram import telegram

app = FastAPI()
app.include_router(telegram)

@app.get("/hello")
def read_root():
    return {"Hello": "World"}
