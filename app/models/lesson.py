from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    asignatura = Column(String, nullable=False)
    curso = Column(String, nullable=False)
    contexto = Column(Text, nullable=True)
    lesson_file_path = Column(String, nullable=True)
    open_ai_thread_id = Column(String, nullable=True)
    open_ai_responses = Column(Text, nullable=True)
