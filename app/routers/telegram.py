from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.example import ExampleCreate, ExampleOut
from app.crud.example import create_example
from app.dependencies import get_db
from uuid import UUID
from typing import List
from app.models.example import Example

router = APIRouter()

@router.post("/examples")
def recibir_ejemplo(example: ExampleCreate, db: Session = Depends(get_db)):
    try:
        nuevo = create_example(db, example)
        return {"status": "ok", "id": str(nuevo.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/telegram/message")
def recibir_texto_desde_telegram(data: ExampleCreate, db: Session = Depends(get_db)):
    try:
        nuevo = create_example(db, data)
        return {"status": "ok", "example_id": str(nuevo.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/lessons/{lesson_id}/examples", response_model=List[ExampleOut])
def listar_ejemplos(lesson_id: UUID, db: Session = Depends(get_db)):
    ejemplos = db.query(Example).filter(Example.lesson_id == lesson_id).order_by(Example.created_at.asc()).all()
    return ejemplos