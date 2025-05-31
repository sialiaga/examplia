from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db import Base

class LessonOA(Base):
    __tablename__ = "lesson_oa"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False)
    oa_id = Column(UUID(as_uuid=True), ForeignKey("oas.id"), nullable=False)
