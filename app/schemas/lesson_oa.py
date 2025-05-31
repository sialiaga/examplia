from pydantic import BaseModel
from uuid import UUID

class LessonOACreate(BaseModel):
    lesson_id: UUID
    oa_id: UUID
