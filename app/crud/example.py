from sqlalchemy.orm import Session
from app.models.example import Example
from app.schemas.example import ExampleCreate

def create_example(db: Session, data: ExampleCreate):
    nuevo = Example(
        lesson_id=data.lesson_id,
        texto=data.texto,
        imagen_url=str(data.imagen_url) if data.imagen_url else None,
        slide_actual=data.slide_actual,
        slide_destino=data.slide_actual + 1
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo