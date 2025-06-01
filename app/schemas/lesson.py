from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class LessonBase(BaseModel):
    nombre: str
    asignatura: str
    curso: str
    contexto: Optional[str] = None
    lesson_file_path: Optional[str] = None

class LessonCreate(LessonBase):
    pass

class LessonOut(LessonBase):
    id: UUID

    model_config = {
        "from_attributes": True
    }
