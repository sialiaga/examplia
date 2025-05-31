from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.example import ExampleCreate
from app.crud.example import create_example
from app.dependencies import get_db

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