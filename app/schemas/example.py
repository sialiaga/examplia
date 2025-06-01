from pydantic import BaseModel, HttpUrl
from uuid import UUID
from typing import Optional
from datetime import datetime

class ExampleCreate(BaseModel):
    lesson_id: UUID
    texto: str
    imagen_url: Optional[HttpUrl] = None
    slide_actual: int  # viene del bot, calcularemos `slide_destino` = actual + 1

class ExampleOut(BaseModel):
    id: UUID
    lesson_id: UUID
    texto: str
    imagen_url: Optional[HttpUrl]
    slide_actual: int
    slide_destino: int
    created_at: datetime

    class Config:
        orm_mode = True