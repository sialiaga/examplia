from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.lesson import LessonCreate, LessonOut
from app.schemas.oa import OACreate, OAOut
from app.schemas.lesson_oa import LessonOACreate
from app.models.lesson import Lesson
from app.models.oa import OA
from app.models.lesson_oa import LessonOA
from app.dependencies import get_db

from typing import List

router = APIRouter(prefix="/lessons", tags=["lessons"])

@router.post("/", response_model=LessonOut)
def crear_leccion(lesson: LessonCreate, db: Session = Depends(get_db)):
    nueva = Lesson(**lesson.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.post("/oas", response_model=None)
def asociar_oa(data: LessonOACreate, db: Session = Depends(get_db)):
    link = LessonOA(lesson_id=data.lesson_id, oa_id=data.oa_id)
    db.add(link)
    db.commit()
    return {"status": "ok"}

@router.post("/oa/", response_model=OAOut)
def crear_oa(oa: OACreate, db: Session = Depends(get_db)):
    nueva = OA(**oa.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/{lesson_id}/oas", response_model=List[OAOut])
def obtener_oas(lesson_id: str, db: Session = Depends(get_db)):
    resultados = (
        db.query(OA)
        .join(LessonOA, OA.id == LessonOA.oa_id)
        .filter(LessonOA.lesson_id == lesson_id)
        .all()
    )
    return resultados
