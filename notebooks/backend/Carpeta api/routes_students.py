from fastapi import APIRouter
from models.student import Student

router = APIRouter()

STUDENTS = {}

@router.post("/")
def create_student(student: Student):
    STUDENTS[student.id] = student
    return {"created": True, "student": student}

@router.get("/{student_id}")
def get_student(student_id: str):
    return STUDENTS.get(student_id, {"error": "not found"})
