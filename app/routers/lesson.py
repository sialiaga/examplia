from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.schemas.lesson import LessonCreate, LessonOut
from app.schemas.oa import OACreate, OAOut
from app.schemas.lesson_oa import LessonOACreate
from app.models.lesson import Lesson
from app.models.oa import OA
from app.models.lesson_oa import LessonOA
from app.dependencies import get_db
from typing import List
from uuid import UUID, uuid4
import shutil
import os

router = APIRouter(prefix="/lessons", tags=["lessons"])

#test function to get all oas
@router.get("/json/oas", response_model=None)
def test_get_oas(db: Session = Depends(get_db)):
    oas = db.query(OA).all()
    # Convert to list of dictionaries with curso: str asignatura: str unidad: str codigo: str description: str
    oas_list = [
        {
            "id": str(oa.id),
            "curso": oa.curso,
            "asignatura": oa.asignatura,
            "unidad": oa.unidad,
            "codigo": oa.codigo,
            "description": oa.description
        } for oa in oas
    ]
    return oas_list

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

@router.delete("/oas", response_model=None)
def eliminar_asociacion_oa(data: LessonOACreate, db: Session = Depends(get_db)):
    link = db.query(LessonOA).filter(
        LessonOA.lesson_id == data.lesson_id,
        LessonOA.oa_id == data.oa_id
    ).first()
    
    if not link:
        raise HTTPException(status_code=404, detail="Association not found")
    
    db.delete(link)
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

@router.get("/{lesson_id}", response_model=LessonOut)
def obtener_leccion(lesson_id: UUID, db: Session = Depends(get_db)):
    leccion = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not leccion:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return leccion

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

@router.post("/{lesson_id}/upload-slide")
async def upload_slide(lesson_id: UUID, file: UploadFile = File(...), db: Session = Depends(get_db)):   
    # Validate file type
    if file.content_type not in ["application/pdf", "application/vnd.ms-powerpoint", "application/vnd.openxmlformats-officedocument.presentationml.presentation"]:
        raise HTTPException(status_code=400, detail="File must be a PDF or PPTX")

    # Resolve absolute path for safe storage
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, "..", "..", "static", "lesson_files")  # two levels up from /app/routers
    os.makedirs(STATIC_DIR, exist_ok=True)

    # Generate filename and save
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid4()}{ext}"
    save_path = os.path.join(STATIC_DIR, filename)

    with open(save_path, "wb") as f:
        f.write(await file.read())

    # Update lesson in DB
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    lesson.lesson_file_path = f"/static/lesson_files/{filename}"
    db.commit()

    return {"message": "File uploaded and associated with lesson"}

@router.get("/{lesson_id}/slide")
async def get_slide(lesson_id: UUID, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson or not lesson.lesson_file_path:
        raise HTTPException(status_code=404, detail="Slide not found")

    # Resolve absolute path for serving
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, "..", "..", "static", "lesson_files")
    file_path = os.path.join(STATIC_DIR, os.path.basename(lesson.lesson_file_path))

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Slide file does not exist")

    return {"file_path": lesson.lesson_file_path}

@router.delete("/{lesson_id}/slide")
async def delete_slide(lesson_id: UUID, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson or not lesson.lesson_file_path:
        raise HTTPException(status_code=404, detail="Slide not found")

    # Resolve absolute path for deletion
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, "..", "..", "static", "lesson_files")
    file_path = os.path.join(STATIC_DIR, os.path.basename(lesson.lesson_file_path))

    if os.path.exists(file_path):
        os.remove(file_path)

    # Clear the file path in the database
    lesson.lesson_file_path = None
    db.commit()

    return {"message": "Slide deleted successfully"}
