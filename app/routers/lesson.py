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
from uuid import UUID
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
def obtener_oas(lesson_id: UUID, db: Session = Depends(get_db)):
    resultados = (
        db.query(OA)
        .join(LessonOA, OA.id == LessonOA.oa_id)
        .filter(LessonOA.lesson_id == lesson_id)
        .all()
    )
    return resultados

@router.get("/", response_model=List[LessonOut])
def listar_lecciones(db: Session = Depends(get_db)):
    return db.query(Lesson).all()

@router.get("/oas/", response_model=List[OAOut])
def listar_oas(db: Session = Depends(get_db)):
    return db.query(OA).all()

@router.get("/oa/{oa_id}/lessons", response_model=List[LessonOut])
def obtener_lecciones_de_oa(oa_id: str, db: Session = Depends(get_db)):
    resultados = (
        db.query(Lesson)
        .join(LessonOA, Lesson.id == LessonOA.lesson_id)
        .filter(LessonOA.oa_id == oa_id)
        .all()
    )
    return resultados