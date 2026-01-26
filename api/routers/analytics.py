from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any
import logging

from database import get_db
from models import User, SimuladoResult, UserAnswer, Question
from schemas import UserAnalytics
from auth import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/results/{user_id}")
async def get_user_results(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Retorna todos os resultados de um usuário"""
    results = db.query(SimuladoResult).filter(
        SimuladoResult.user_id == user_id
    ).all()
    
    return results

@router.get("/analytics/{user_id}", response_model=UserAnalytics)
async def get_user_analytics(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna analytics completo do usuário:
    - Total de simulados
    - Média de score
    - Disciplinas fortes/fracas
    - Tempo médio por questão
    - Progresso temporal
    """
    try:
        # Total de simulados
        total_simulados = db.query(func.count(SimuladoResult.id)).filter(
            SimuladoResult.user_id == user_id
        ).scalar()
        
        # Média de score
        media_score = db.query(func.avg(SimuladoResult.score)).filter(
            SimuladoResult.user_id == user_id
        ).scalar() or 0.0
        
        # Análise por disciplina
        answers = db.query(
            Question.disciplina,
            func.count(UserAnswer.id).label('total'),
            func.sum(func.cast(UserAnswer.is_correct, db.Integer)).label('acertos')
        ).join(Question).filter(
            UserAnswer.user_id == user_id
        ).group_by(Question.disciplina).all()
        
        disciplinas_stats = []
        for disc, total, acertos in answers:
            taxa = (acertos / total * 100) if total > 0 else 0
            disciplinas_stats.append({
                'disciplina': disc,
                'taxa_acerto': taxa,
                'total_questoes': total
            })
        
        disciplinas_stats.sort(key=lambda x: x['taxa_acerto'], reverse=True)
        disciplinas_fortes = [d['disciplina'] for d in disciplinas_stats[:3]]
        disciplinas_fracas = [d['disciplina'] for d in disciplinas_stats[-3:]]
        
        # Tempo médio
        tempo_medio = db.query(func.avg(UserAnswer.tempo_resposta)).filter(
            UserAnswer.user_id == user_id,
            UserAnswer.tempo_resposta.isnot(None)
        ).scalar() or 0.0
        
        # Progresso temporal
        progresso = db.query(
            SimuladoResult.completed_at,
            SimuladoResult.score
        ).filter(
            SimuladoResult.user_id == user_id
        ).order_by(SimuladoResult.completed_at).all()
        
        progresso_temporal = [
            {
                'data': str(p[0]),
                'score': p[1]
            }
            for p in progresso
        ]
        
        return UserAnalytics(
            total_simulados=total_simulados,
            media_score=float(media_score),
            disciplinas_fortes=disciplinas_fortes,
            disciplinas_fracas=disciplinas_fracas,
            tempo_medio_questao=float(tempo_medio),
            progresso_temporal=progresso_temporal
        )
        
    except Exception as e:
        logger.error(f"Error getting analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/suggestions")
async def get_study_suggestions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna sugestões de estudo baseadas no desempenho.
    Implementa algoritmo SRS-like.
    """
    from services.adaptive_service import AdaptiveService
    
    service = AdaptiveService(db)
    suggestions = service.get_study_plan(current_user.id)
    
    return suggestions
