from app.db import Base, engine

from app.models.lesson import Lesson
from app.models.oa import OA
from app.models.lesson_oa import LessonOA
from app.models.example import Example

print("Creando tablas...")
Base.metadata.create_all(bind=engine)
print("Listo ✅")
