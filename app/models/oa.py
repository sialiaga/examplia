from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db import Base

class OA(Base):
    __tablename__ = "oas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    curso = Column(String, nullable=False)
    asignatura = Column(String, nullable=False)
    unidad = Column(String, nullable=False)
    codigo = Column(String, nullable=False)
    description = Column(String, nullable=False)
