from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.db import Base  # Asegúrate de que tengas esto definido en db/__init__.py

class Example(Base):
    __tablename__ = "examples"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False)
    texto = Column(Text, nullable=False)
    imagen_url = Column(String, nullable=True)
    slide_actual = Column(Integer, nullable=False)
    slide_destino = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
