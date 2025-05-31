from sqlalchemy.orm import Session
from app.models.example import Example
from app.schemas.example import ExampleCreate

def create_example(db: Session, example_in: ExampleCreate):
    slide_destino = example_in.slide_actual + 1
    db_example = Example(
        lesson_id=example_in.lesson_id,
        texto=example_in.texto,
        imagen_url=example_in.imagen_url,
        slide_destino=slide_destino
    )
    db.add(db_example)
    db.commit()
    db.refresh(db_example)
    return db_example
