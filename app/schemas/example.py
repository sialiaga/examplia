from pydantic import BaseModel, HttpUrl
from uuid import UUID
from typing import Optional

class ExampleCreate(BaseModel):
    lesson_id: UUID
    texto: str
    imagen_url: Optional[HttpUrl] = None
    slide_actual: int  # viene del bot, calcularemos `slide_destino` = actual + 1

