"""
Router para Sistema de Aprendizado Adaptativo
Endpoints para análise de performance e recomendações personalizadas
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from auth import get_current_user
from models import User
from services.adaptive_learning_engine import AdaptiveLearningEngine

router = APIRouter()


@router.get("/adaptive/analyze")
async def analyze_performance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analisa o desempenho completo do usuário
    
    Retorna:
    - Tópicos fracos e fortes
    - Padrão de aprendizado
    - Dificuldade recomendada
    - Acurácia geral
    """
    engine = AdaptiveLearningEngine(db)
    analysis = engine.analyze_user_performance(current_user.id)
    
    return analysis


@router.get("/adaptive/study-plan")
async def get_study_plan(
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Gera plano de estudos personalizado
    
    Args:
        days: Número de dias do plano (padrão: 7)
    
    Retorna:
    - Plano diário com tópicos priorizados
    - Metas de questões
    - Estimativa de melhoria
    """
    if days < 1 or days > 30:
        raise HTTPException(
            status_code=400,
            detail="Número de dias deve estar entre 1 e 30"
        )
    
    engine = AdaptiveLearningEngine(db)
    plan = engine.generate_personalized_study_plan(current_user.id, days)
    
    return plan


@router.get("/adaptive/next-questions")
async def get_next_questions(
    quantity: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna próximas questões recomendadas baseado no perfil
    
    Args:
        quantity: Número de questões (padrão: 10, máx: 50)
    
    Retorna:
    - Lista de questões personalizadas
    - Focadas em pontos fracos
    - Evita questões recentes
    """
    if quantity < 1 or quantity > 50:
        raise HTTPException(
            status_code=400,
            detail="Quantidade deve estar entre 1 e 50"
        )
    
    engine = AdaptiveLearningEngine(db)
    questions = engine.get_next_recommended_questions(current_user.id, quantity)
    
    return {
        "total": len(questions),
        "questions": [
            {
                "id": q.id,
                "disciplina": q.disciplina,
                "topico": q.topico,
                "subtopico": q.subtopico,
                "enunciado": q.enunciado,
                "dificuldade": q.dificuldade,
                "estimativa_tempo": q.estimativa_tempo
            }
            for q in questions
        ]
    }


@router.get("/adaptive/predict-performance")
async def predict_performance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Prevê desempenho do usuário em prova real
    
    Retorna:
    - Nota estimada
    - Probabilidade de aprovação
    - Status de performance
    - Recomendações
    """
    engine = AdaptiveLearningEngine(db)
    prediction = engine.predict_exam_performance(current_user.id)
    
    return prediction
