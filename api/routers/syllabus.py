from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from database import get_db
from models import Syllabus, Topic
from schemas import SyllabusResponse
from services.parser import SyllabusParser

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload-syllabus", response_model=SyllabusResponse)
async def upload_syllabus(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload e parse de edital (TXT ou PDF).
    Retorna: 'Conteúdo programático recebido'
    """
    try:
        # Ler conteúdo do arquivo
        content = await file.read()
        
        # Detectar tipo e fazer parse
        parser = SyllabusParser()
        if file.filename.endswith('.pdf'):
            text_content = parser.extract_from_pdf(content)
        else:
            text_content = content.decode('utf-8')
        
        # Parse hierárquico
        parsed_structure = parser.parse_hierarchical(text_content)
        
        # Salvar no banco
        syllabus = Syllabus(
            filename=file.filename,
            content=text_content,
            parsed_structure=parsed_structure,
            source_reference=file.filename
        )
        db.add(syllabus)
        db.commit()
        db.refresh(syllabus)
        
        # Criar tópicos
        for disc in parsed_structure.get('disciplinas', []):
            for top in disc.get('topicos', []):
                topic = Topic(
                    syllabus_id=syllabus.id,
                    disciplina=disc['nome'],
                    topico=top['nome'],
                    subtopico=top.get('subtopico'),
                    reference=top.get('reference')
                )
                db.add(topic)
        
        db.commit()
        
        logger.info(f"Syllabus uploaded: {file.filename}")
        
        return SyllabusResponse(
            id=syllabus.id,
            filename=syllabus.filename,
            parsed_structure=parsed_structure,
            uploaded_at=syllabus.uploaded_at,
            message="Conteúdo programático recebido"
        )
        
    except Exception as e:
        logger.error(f"Error uploading syllabus: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/syllabus/{syllabus_id}")
async def get_syllabus(syllabus_id: int, db: Session = Depends(get_db)):
    syllabus = db.query(Syllabus).filter(Syllabus.id == syllabus_id).first()
    if not syllabus:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    return syllabus

@router.get("/topics")
async def list_topics(db: Session = Depends(get_db)):
    topics = db.query(Topic).all()
    return topics
