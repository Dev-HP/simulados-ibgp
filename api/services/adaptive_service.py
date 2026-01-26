import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from models import UserAnswer, Question, QAStatus

logger = logging.getLogger(__name__)

class AdaptiveService:
    """
    Serviço de treino adaptativo com algoritmo SRS-like.
    Prioriza questões com baixo acerto e espaçamento baseado em desempenho.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_study_plan(self, user_id: int) -> Dict[str, Any]:
        """
        Retorna plano de estudo adaptativo para o usuário.
        Baseado em:
        - Desempenho por tópico
        - Espaçamento (SRS)
        - Priorização de tópicos fracos
        """
        # Analisar desempenho
        performance = self._analyze_performance(user_id)
        
        # Identificar tópicos prioritários
        priority_topics = self._identify_priority_topics(performance)
        
        # Selecionar questões para revisão
        review_questions = self._select_review_questions(user_id, priority_topics)
        
        # Selecionar novas questões
        new_questions = self._select_new_questions(user_id, priority_topics)
        
        return {
            'performance_summary': performance,
            'priority_topics': priority_topics,
            'review_questions': review_questions,
            'new_questions': new_questions,
            'daily_goal': self._calculate_daily_goal(performance)
        }
    
    def _analyze_performance(self, user_id: int) -> Dict[str, Any]:
        """Analisa desempenho do usuário por tópico"""
        # Buscar todas as respostas
        answers = self.db.query(
            Question.disciplina,
            Question.topico,
            func.count(UserAnswer.id).label('total'),
            func.sum(func.cast(UserAnswer.is_correct, self.db.Integer)).label('acertos'),
            func.avg(UserAnswer.tempo_resposta).label('tempo_medio')
        ).join(Question).filter(
            UserAnswer.user_id == user_id
        ).group_by(
            Question.disciplina,
            Question.topico
        ).all()
        
        performance = {}
        for disc, top, total, acertos, tempo in answers:
            key = f"{disc}_{top}"
            taxa = (acertos / total * 100) if total > 0 else 0
            
            performance[key] = {
                'disciplina': disc,
                'topico': top,
                'total_questoes': total,
                'acertos': acertos,
                'taxa_acerto': taxa,
                'tempo_medio': float(tempo) if tempo else 0,
                'nivel': self._classify_level(taxa)
            }
        
        return performance
    
    def _classify_level(self, taxa_acerto: float) -> str:
        """Classifica nível de domínio"""
        if taxa_acerto >= 80:
            return "avançado"
        elif taxa_acerto >= 60:
            return "intermediário"
        else:
            return "iniciante"
    
    def _identify_priority_topics(
        self,
        performance: Dict[str, Any],
        threshold: float = 60.0
    ) -> List[Dict[str, Any]]:
        """
        Identifica tópicos prioritários (taxa < threshold).
        Ordena por: taxa_acerto (asc) e total_questoes (desc)
        """
        priority = []
        
        for key, stats in performance.items():
            if stats['taxa_acerto'] < threshold:
                priority.append({
                    'disciplina': stats['disciplina'],
                    'topico': stats['topico'],
                    'taxa_acerto': stats['taxa_acerto'],
                    'prioridade': self._calculate_priority(stats)
                })
        
        # Ordenar por prioridade
        priority.sort(key=lambda x: x['prioridade'], reverse=True)
        
        return priority[:5]  # Top 5 prioridades
    
    def _calculate_priority(self, stats: Dict[str, Any]) -> float:
        """
        Calcula prioridade do tópico.
        Quanto menor a taxa e maior o número de questões, maior a prioridade.
        """
        taxa = stats['taxa_acerto']
        total = stats['total_questoes']
        
        # Prioridade inversa à taxa, proporcional ao total
        priority = (100 - taxa) * (1 + total / 100)
        
        return priority
    
    def _select_review_questions(
        self,
        user_id: int,
        priority_topics: List[Dict[str, Any]],
        limit: int = 10
    ) -> List[int]:
        """
        Seleciona questões para revisão baseado em SRS.
        Prioriza:
        - Questões erradas
        - Questões antigas (espaçamento)
        - Tópicos prioritários
        """
        if not priority_topics:
            return []
        
        # Buscar questões erradas nos tópicos prioritários
        topic_filters = [
            (pt['disciplina'], pt['topico']) for pt in priority_topics
        ]
        
        # Questões erradas recentemente
        wrong_answers = self.db.query(UserAnswer).filter(
            UserAnswer.user_id == user_id,
            UserAnswer.is_correct == False
        ).order_by(UserAnswer.answered_at.desc()).limit(limit * 2).all()
        
        # Filtrar por tópicos prioritários
        review_ids = []
        for answer in wrong_answers:
            question = answer.question
            if (question.disciplina, question.topico) in topic_filters:
                # Verificar espaçamento (SRS)
                if self._should_review(answer):
                    review_ids.append(question.id)
                    if len(review_ids) >= limit:
                        break
        
        return review_ids
    
    def _should_review(self, answer: UserAnswer) -> bool:
        """
        Determina se questão deve ser revisada (SRS).
        Baseado em: tempo desde última resposta e número de erros.
        """
        # Calcular intervalo desde última resposta
        days_since = (datetime.utcnow() - answer.answered_at).days
        
        # Buscar histórico da questão
        attempts = self.db.query(UserAnswer).filter(
            UserAnswer.user_id == answer.user_id,
            UserAnswer.question_id == answer.question_id
        ).count()
        
        # Intervalo aumenta com tentativas corretas
        if answer.is_correct:
            required_interval = 2 ** attempts  # Exponencial
        else:
            required_interval = 1  # Revisar logo se errou
        
        return days_since >= required_interval
    
    def _select_new_questions(
        self,
        user_id: int,
        priority_topics: List[Dict[str, Any]],
        limit: int = 10
    ) -> List[int]:
        """
        Seleciona novas questões dos tópicos prioritários.
        """
        if not priority_topics:
            return []
        
        # Buscar questões não respondidas
        answered_ids = self.db.query(UserAnswer.question_id).filter(
            UserAnswer.user_id == user_id
        ).subquery()
        
        new_questions = []
        
        for topic in priority_topics:
            questions = self.db.query(Question).filter(
                Question.disciplina == topic['disciplina'],
                Question.topico == topic['topico'],
                Question.qa_status == QAStatus.APPROVED,
                ~Question.id.in_(answered_ids)
            ).limit(limit // len(priority_topics) + 1).all()
            
            new_questions.extend([q.id for q in questions])
        
        return new_questions[:limit]
    
    def _calculate_daily_goal(self, performance: Dict[str, Any]) -> Dict[str, int]:
        """
        Calcula meta diária baseada no desempenho.
        """
        # Média de taxa de acerto
        if not performance:
            return {'review': 10, 'new': 10}
        
        avg_taxa = sum(p['taxa_acerto'] for p in performance.values()) / len(performance)
        
        # Ajustar metas
        if avg_taxa < 50:
            return {'review': 15, 'new': 5}
        elif avg_taxa < 70:
            return {'review': 10, 'new': 10}
        else:
            return {'review': 5, 'new': 15}
