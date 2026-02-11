from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .core.video_selector import pipeline

router = APIRouter()

class StudyRequest(BaseModel):
    syllabus: str
    student_bio: str
    language: str
    time_limit: str

@router.post("/generate")
def generate_video(data: StudyRequest):
    try:
        result = pipeline(
            syllabus=data.syllabus,
            student_bio=data.student_bio,
            language=data.language,
            time_limit=data.time_limit
        )
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
