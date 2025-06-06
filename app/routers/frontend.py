from fastapi import FastAPI, Request, APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.routers.lesson import listar_lecciones, obtener_leccion
from app.dependencies import get_db
from uuid import UUID

router = APIRouter(prefix="/frontend", tags=["frontend"])

templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("Login.html", {"request": request})

@router.get("/home", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    # Call the backend function to get lessons
    lessons = listar_lecciones(db=db)
    lessons_data = [
        {
            "id": str(lesson.id),
            "name": lesson.nombre,
            "subject": lesson.asignatura,
            "course": lesson.curso,
            "description": lesson.contexto,
            "lesson_file_path": lesson.lesson_file_path
        }
        for lesson in lessons
    ]

    print("Lessons fetched from backend:", lessons_data)
    return templates.TemplateResponse("Home.html", {"request": request, "lessons": lessons_data})

@router.get("/lesson/{lesson_id}", response_class=HTMLResponse)
def view_lesson(request: Request, lesson_id: UUID, db: Session = Depends(get_db)):
    print(f"Fetching lesson with ID: {lesson_id}")
    try:
        # Call the existing endpoint function directly
        lesson = obtener_leccion(lesson_id=lesson_id, db=db)

        # Convert LessonOut model to dict for template
        lesson_data = {
            "id": str(lesson.id),
            "name": lesson.nombre,
            "subject": lesson.asignatura,
            "course": lesson.curso,
            "description": lesson.contexto,
            "lesson_file_path": lesson.lesson_file_path
        }

        return templates.TemplateResponse("LessonDetail.html", {
            "request": request,
            "lesson": lesson_data
        })
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internail server error: {str(e)}")
    
#get lesson data, and lesson file path, go to the teach.html page
@router.get("/lesson/{lesson_id}/teach", response_class=HTMLResponse)
def teach_lesson(request: Request, lesson_id: UUID, db: Session = Depends(get_db)):
    print(f"Fetching lesson for teaching with ID: {lesson_id}")
    try:
        # Call the existing endpoint function directly
        lesson = obtener_leccion(lesson_id=lesson_id, db=db)

        # Convert LessonOut model to dict for template
        lesson_data = {
            "id": str(lesson.id),
            "name": lesson.nombre,
            "subject": lesson.asignatura,
            "course": lesson.curso,
            "description": lesson.contexto,
            "lesson_file_path": lesson.lesson_file_path
        }

        return templates.TemplateResponse("Teach.html", {
            "request": request,
            "lesson": lesson_data
        })
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.get("/test", response_class=HTMLResponse)
def test_page(request: Request):
    """
    Test page to verify that the frontend is working correctly.
    """
    return templates.TemplateResponse("Test.html", {"request": request})
