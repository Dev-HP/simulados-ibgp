from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from database import get_db
from models import Question, Topic
from schemas import QuestionResponse, QuestionCreate, GenerateBankRequest
from services.question_generator import QuestionGenerator

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate-bank")
async def generate_question_bank(
    request: GenerateBankRequest,
    db: Session = Depends(get_db)
):
    """
    Gera banco de questões baseado nos tópicos do edital.
    Mínimo 30 questões por tópico amplo, 10 para tópicos pequenos.
    """
    try:
        generator = QuestionGenerator(db)
        
        # Buscar tópicos
        topics = db.query(Topic).all()
        if not topics:
            raise HTTPException(status_code=400, detail="No topics found. Upload syllabus first.")
        
        # Gerar questões
        generated_count = generator.generate_for_topics(
            topics=topics,
            min_questions=request.min_questions_per_topic,
            seeds=request.seeds
        )
        
        return {
            "message": "Question bank generated successfully",
            "total_questions": generated_count,
            "topics_covered": len(topics)
        }
        
    except Exception as e:
        logger.error(f"Error generating question bank: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/questions", response_model=List[QuestionResponse])
async def list_questions(
    disciplina: Optional[str] = None,
    topico: Optional[str] = None,
    dificuldade: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Question)
    
    if disciplina:
        query = query.filter(Question.disciplina == disciplina)
    if topico:
        query = query.filter(Question.topico == topico)
    if dificuldade:
        query = query.filter(Question.dificuldade == dificuldade)
    
    questions = query.offset(skip).limit(limit).all()
    return questions

@router.get("/questions/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.post("/questions", response_model=QuestionResponse)
async def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db)
):
    """Criar questão manualmente"""
    db_question = Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question
