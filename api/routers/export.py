from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
import io

from database import get_db
from models import Question
from services.export_service import ExportService

router = APIRouter()

@router.get("/export/gift")
async def export_gift(
    disciplina: Optional[str] = None,
    topico: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Export questões em formato GIFT (Moodle)"""
    query = db.query(Question)
    
    if disciplina:
        query = query.filter(Question.disciplina == disciplina)
    if topico:
        query = query.filter(Question.topico == topico)
    
    questions = query.all()
    
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    
    service = ExportService()
    content = service.export_gift(questions)
    
    return StreamingResponse(
        io.StringIO(content),
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=questions.gift"}
    )

@router.get("/export/csv")
async def export_csv(
    disciplina: Optional[str] = None,
    topico: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Export questões em formato CSV"""
    query = db.query(Question)
    
    if disciplina:
        query = query.filter(Question.disciplina == disciplina)
    if topico:
        query = query.filter(Question.topico == topico)
    
    questions = query.all()
    
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    
    service = ExportService()
    content = service.export_csv(questions)
    
    return StreamingResponse(
        io.StringIO(content),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=questions.csv"}
    )

@router.get("/export/json")
async def export_json(
    disciplina: Optional[str] = None,
    topico: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Export questões em formato JSON"""
    query = db.query(Question)
    
    if disciplina:
        query = query.filter(Question.disciplina == disciplina)
    if topico:
        query = query.filter(Question.topico == topico)
    
    questions = query.all()
    
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    
    service = ExportService()
    content = service.export_json(questions)
    
    return StreamingResponse(
        io.StringIO(content),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=questions.json"}
    )
