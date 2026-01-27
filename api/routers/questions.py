from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
import os

from database import get_db
from models import Question, Topic
from schemas import QuestionResponse, QuestionCreate, GenerateBankRequest
from services.question_generator import QuestionGenerator
from services.gemini_generator import GeminiQuestionGenerator
from services.question_importer import QuestionImporter

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

@router.post("/import-questions")
async def import_questions(
    file: UploadFile = File(...),
    disciplina: str = "Informática",
    db: Session = Depends(get_db)
):
    """
    Importa questões de provas reais (PDF ou TXT).
    
    Formato esperado:
    QUESTÃO 1
    Enunciado...
    A) alternativa
    B) alternativa
    C) alternativa
    D) alternativa
    Gabarito: A
    """
    try:
        importer = QuestionImporter(db)
        content = await file.read()
        
        if file.filename.endswith('.pdf'):
            questions = importer.import_from_pdf(content, file.filename, disciplina)
        else:
            text = content.decode('utf-8')
            questions = importer.import_from_text(text, file.filename, disciplina)
        
        return {
            "message": "Questions imported successfully",
            "total_imported": len(questions),
            "source": file.filename
        }
        
    except Exception as e:
        logger.error(f"Error importing questions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-with-ai")
async def generate_with_ai(
    topic_id: int,
    quantity: int = 10,
    difficulty: Optional[str] = None,
    use_references: bool = True,
    db: Session = Depends(get_db)
):
    """
    Gera questões usando Gemini Pro baseadas em questões reais.
    
    Parâmetros:
    - topic_id: ID do tópico
    - quantity: Quantidade de questões a gerar
    - difficulty: FACIL, MEDIO ou DIFICIL (opcional)
    - use_references: Usar questões reais como referência
    """
    try:
        # Verificar se GEMINI_API_KEY está configurada
        if not os.getenv('GEMINI_API_KEY'):
            raise HTTPException(
                status_code=400,
                detail="GEMINI_API_KEY não configurada. Configure no arquivo .env"
            )
        
        # Buscar tópico
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")
        
        # Buscar questões de referência
        reference_questions = []
        if use_references:
            refs = db.query(Question).filter(
                Question.disciplina == topic.disciplina
            ).limit(5).all()
            reference_questions = [
                {
                    'enunciado': q.enunciado,
                    'alternativa_a': q.alternativa_a,
                    'alternativa_b': q.alternativa_b,
                    'alternativa_c': q.alternativa_c,
                    'alternativa_d': q.alternativa_d,
                    'gabarito': q.gabarito,
                    'explicacao_detalhada': q.explicacao_detalhada
                }
                for q in refs
            ]
        
        # Gerar com Gemini
        generator = GeminiQuestionGenerator(db)
        questions = generator.generate_questions_with_ai(
            topic=topic,
            quantity=quantity,
            reference_questions=reference_questions,
            difficulty=difficulty
        )
        
        return {
            "message": "Questions generated with AI successfully",
            "total_generated": len(questions),
            "topic": topic.topico,
            "references_used": len(reference_questions)
        }
        
    except Exception as e:
        logger.error(f"Error generating with AI: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/improve-question/{question_id}")
async def improve_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    """
    Melhora uma questão existente usando Gemini Pro.
    """
    try:
        if not os.getenv('GEMINI_API_KEY'):
            raise HTTPException(
                status_code=400,
                detail="GEMINI_API_KEY não configurada"
            )
        
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        generator = GeminiQuestionGenerator(db)
        improved = generator.improve_existing_question(question)
        
        if improved:
            return {
                "message": "Question improved successfully",
                "question_id": question_id
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to improve question")
            
    except Exception as e:
        logger.error(f"Error improving question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/gemini-stats")
async def get_gemini_stats():
    """
    Retorna estatísticas de uso da API Gemini.
    Mostra limites do free tier e uso atual.
    """
    from services.rate_limiter import gemini_rate_limiter
    
    stats = gemini_rate_limiter.get_stats()
    
    return {
        "status": "ok",
        "tier": "free",
        "limits": {
            "per_minute": stats['limit_per_minute'],
            "per_day": stats['limit_per_day']
        },
        "usage": {
            "last_minute": stats['requests_last_minute'],
            "today": stats['requests_today'],
            "total": stats['total_requests'],
            "blocked": stats['blocked_requests']
        },
        "remaining": {
            "minute": stats['remaining_minute'],
            "day": stats['remaining_day']
        },
        "percentage": {
            "minute": round(stats['usage_percentage_minute'], 2),
            "day": round(stats['usage_percentage_day'], 2)
        },
        "warnings": [
            "⚠️ Limite por minuto atingido" if stats['remaining_minute'] < 5 else None,
            "⚠️ Limite diário próximo" if stats['remaining_day'] < 100 else None
        ]
    }
