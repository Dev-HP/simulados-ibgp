from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from database import get_db
from models import Simulado, SimuladoQuestion, SimuladoResult, UserAnswer, User, Question
from schemas import SimuladoCreate, SimuladoResponse, AnswerSubmit, AnswerFeedback, SimuladoResultResponse
from services.simulado_service import SimuladoService
from auth import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/create-simulado", response_model=SimuladoResponse)
async def create_simulado(
    request: SimuladoCreate,
    db: Session = Depends(get_db)
):
    """
    Cria simulado configurável.
    Parâmetros: numero_questoes, disciplinas, tempo_total, pesos, aleatorizacao_por_topico, dificuldade_alvo
    """
    try:
        service = SimuladoService(db)
        simulado = service.create_simulado(request)
        
        return SimuladoResponse(
            id=simulado.id,
            nome=simulado.nome,
            descricao=simulado.descricao,
            numero_questoes=simulado.numero_questoes,
            tempo_total=simulado.tempo_total,
            disciplinas=simulado.disciplinas,
            is_oficial=simulado.is_oficial,
            created_at=simulado.created_at
        )
        
    except Exception as e:
        logger.error(f"Error creating simulado: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/simulados", response_model=List[SimuladoResponse])
async def list_simulados(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    simulados = db.query(Simulado).offset(skip).limit(limit).all()
    return simulados

@router.get("/simulados/{simulado_id}")
async def get_simulado(simulado_id: int, db: Session = Depends(get_db)):
    simulado = db.query(Simulado).filter(Simulado.id == simulado_id).first()
    if not simulado:
        raise HTTPException(status_code=404, detail="Simulado not found")
    
    # Buscar questões
    questions = db.query(Question).join(SimuladoQuestion).filter(
        SimuladoQuestion.simulado_id == simulado_id
    ).order_by(SimuladoQuestion.ordem).all()
    
    return {
        "simulado": simulado,
        "questions": questions
    }

@router.post("/simulados/{simulado_id}/answer", response_model=AnswerFeedback)
async def submit_answer(
    simulado_id: int,
    answer: AnswerSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submete resposta e retorna feedback imediato.
    """
    try:
        service = SimuladoService(db)
        feedback = service.process_answer(
            user_id=current_user.id,
            simulado_id=simulado_id,
            question_id=answer.question_id,
            resposta=answer.resposta,
            tempo_resposta=answer.tempo_resposta
        )
        
        return feedback
        
    except Exception as e:
        logger.error(f"Error submitting answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/simulados/{simulado_id}/finalize", response_model=SimuladoResultResponse)
async def finalize_simulado(
    simulado_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Finaliza simulado e gera relatório completo.
    """
    try:
        service = SimuladoService(db)
        result = service.finalize_simulado(current_user.id, simulado_id)
        
        return result
        
    except Exception as e:
        logger.error(f"Error finalizing simulado: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
