"""
Sistema de Aprendizado Adaptativo Inteligente
Analisa performance do usuário e personaliza o estudo
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

from models import UserAnswer, Question, Topic, SimuladoResult, User

logger = logging.getLogger(__name__)


class AdaptiveLearningEngine:
    """
    Motor de aprendizado adaptativo que personaliza a experiência de estudo
    baseado no desempenho individual do usuário
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def analyze_user_performance(self, user_id: int) -> Dict:
        """
        Analisa o desempenho completo do usuário
        
        Returns:
            Dict com análise detalhada:
            - weak_topics: Tópicos com baixo desempenho
            - strong_topics: Tópicos com alto desempenho
            - learning_pattern: Padrão de aprendizado identificado
            - recommended_difficulty: Dificuldade recomendada
            - study_time_optimal: Melhor horário de estudo
        """
        
        # Buscar todas as respostas do usuário
        answers = self.db.query(UserAnswer).filter(
            UserAnswer.user_id == user_id
        ).all()
        
        if not answers:
            return {
                "status": "insufficient_data",
                "message": "Faça pelo menos 10 questões para análise personalizada",
                "weak_topics": [],
                "strong_topics": [],
                "learning_pattern": "unknown",
                "recommended_difficulty": "MEDIO"
            }
        
        # Análise por tópico
        topic_performance = {}
        
        for answer in answers:
            question = answer.question
            topic_key = f"{question.disciplina}:{question.topico}"
            
            if topic_key not in topic_performance:
                topic_performance[topic_key] = {
                    "correct": 0,
                    "total": 0,
                    "avg_time": 0,
                    "disciplina": question.disciplina,
                    "topico": question.topico
                }
            
            topic_performance[topic_key]["total"] += 1
            if answer.is_correct:
                topic_performance[topic_key]["correct"] += 1
            
            if answer.tempo_resposta:
                topic_performance[topic_key]["avg_time"] += answer.tempo_resposta
        
        # Calcular percentuais
        for topic_key in topic_performance:
            total = topic_performance[topic_key]["total"]
            topic_performance[topic_key]["accuracy"] = (
                topic_performance[topic_key]["correct"] / total * 100
            )
            topic_performance[topic_key]["avg_time"] = (
                topic_performance[topic_key]["avg_time"] / total
            )
        
        # Identificar tópicos fracos (< 60% acerto)
        weak_topics = [
            {
                "disciplina": data["disciplina"],
                "topico": data["topico"],
                "accuracy": data["accuracy"],
                "total_questions": data["total"]
            }
            for topic_key, data in topic_performance.items()
            if data["accuracy"] < 60 and data["total"] >= 3
        ]
        
        # Ordenar por pior desempenho
        weak_topics.sort(key=lambda x: x["accuracy"])
        
        # Identificar tópicos fortes (> 80% acerto)
        strong_topics = [
            {
                "disciplina": data["disciplina"],
                "topico": data["topico"],
                "accuracy": data["accuracy"],
                "total_questions": data["total"]
            }
            for topic_key, data in topic_performance.items()
            if data["accuracy"] >= 80 and data["total"] >= 3
        ]
        
        # Ordenar por melhor desempenho
        strong_topics.sort(key=lambda x: x["accuracy"], reverse=True)
        
        # Identificar padrão de aprendizado
        learning_pattern = self._identify_learning_pattern(answers)
        
        # Recomendar dificuldade
        overall_accuracy = sum(1 for a in answers if a.is_correct) / len(answers) * 100
        
        if overall_accuracy >= 85:
            recommended_difficulty = "DIFICIL"
        elif overall_accuracy >= 65:
            recommended_difficulty = "MEDIO"
        else:
            recommended_difficulty = "FACIL"
        
        return {
            "status": "success",
            "total_questions_answered": len(answers),
            "overall_accuracy": round(overall_accuracy, 1),
            "weak_topics": weak_topics[:5],  # Top 5 piores
            "strong_topics": strong_topics[:5],  # Top 5 melhores
            "learning_pattern": learning_pattern,
            "recommended_difficulty": recommended_difficulty,
            "topics_analyzed": len(topic_performance)
        }
    
    def _identify_learning_pattern(self, answers: List[UserAnswer]) -> str:
        """
        Identifica o padrão de aprendizado do usuário
        
        Padrões possíveis:
        - improving: Melhorando com o tempo
        - declining: Piorando com o tempo
        - consistent: Desempenho consistente
        - volatile: Desempenho muito variável
        """
        
        if len(answers) < 10:
            return "insufficient_data"
        
        # Dividir em 3 períodos
        third = len(answers) // 3
        
        first_third = answers[:third]
        second_third = answers[third:2*third]
        last_third = answers[2*third:]
        
        # Calcular acurácia de cada período
        acc_first = sum(1 for a in first_third if a.is_correct) / len(first_third) * 100
        acc_second = sum(1 for a in second_third if a.is_correct) / len(second_third) * 100
        acc_last = sum(1 for a in last_third if a.is_correct) / len(last_third) * 100
        
        # Identificar tendência
        if acc_last > acc_first + 10:
            return "improving"
        elif acc_last < acc_first - 10:
            return "declining"
        elif abs(acc_last - acc_first) < 5:
            return "consistent"
        else:
            return "volatile"
    
    def generate_personalized_study_plan(self, user_id: int, days: int = 7) -> Dict:
        """
        Gera um plano de estudos personalizado baseado na análise
        
        Args:
            user_id: ID do usuário
            days: Número de dias do plano (padrão: 7)
        
        Returns:
            Plano de estudos com tópicos priorizados e metas diárias
        """
        
        analysis = self.analyze_user_performance(user_id)
        
        if analysis["status"] == "insufficient_data":
            return {
                "status": "insufficient_data",
                "message": "Complete mais questões para gerar plano personalizado",
                "recommendation": "Faça pelo menos 1 prova completa primeiro"
            }
        
        # Priorizar tópicos fracos
        weak_topics = analysis["weak_topics"]
        
        # Criar plano diário
        daily_plan = []
        
        for day in range(1, days + 1):
            # Alternar entre revisar pontos fracos e praticar novos tópicos
            if day % 2 == 1:  # Dias ímpares: focar em pontos fracos
                if weak_topics:
                    topic_idx = (day // 2) % len(weak_topics)
                    topic = weak_topics[topic_idx]
                    
                    daily_plan.append({
                        "day": day,
                        "focus": "weak_topic",
                        "disciplina": topic["disciplina"],
                        "topico": topic["topico"],
                        "current_accuracy": topic["accuracy"],
                        "target_accuracy": 70,
                        "recommended_questions": 15,
                        "difficulty": "FACIL" if topic["accuracy"] < 40 else "MEDIO",
                        "tip": f"Foque em entender os conceitos básicos de {topic['topico']}"
                    })
            else:  # Dias pares: praticar mix de tópicos
                daily_plan.append({
                    "day": day,
                    "focus": "mixed_practice",
                    "recommended_questions": 20,
                    "difficulty": analysis["recommended_difficulty"],
                    "tip": "Faça uma prova completa para consolidar conhecimento"
                })
        
        return {
            "status": "success",
            "user_id": user_id,
            "plan_duration_days": days,
            "overall_accuracy": analysis["overall_accuracy"],
            "learning_pattern": analysis["learning_pattern"],
            "daily_plan": daily_plan,
            "priority_topics": weak_topics[:3],
            "estimated_improvement": self._estimate_improvement(analysis)
        }
    
    def _estimate_improvement(self, analysis: Dict) -> str:
        """Estima melhoria esperada seguindo o plano"""
        
        current_acc = analysis["overall_accuracy"]
        
        if current_acc < 50:
            return "Seguindo o plano, você pode melhorar 20-30% em 2 semanas"
        elif current_acc < 70:
            return "Seguindo o plano, você pode melhorar 15-20% em 2 semanas"
        else:
            return "Seguindo o plano, você pode melhorar 10-15% em 2 semanas"
    
    def get_next_recommended_questions(
        self, 
        user_id: int, 
        quantity: int = 10
    ) -> List[Question]:
        """
        Retorna as próximas questões recomendadas baseado no perfil do usuário
        
        Algoritmo:
        1. Identifica tópicos fracos
        2. Seleciona questões desses tópicos
        3. Ajusta dificuldade baseado no desempenho
        4. Evita questões já respondidas recentemente
        """
        
        analysis = self.analyze_user_performance(user_id)
        
        # Buscar questões já respondidas (últimas 50)
        answered_ids = [
            a.question_id for a in 
            self.db.query(UserAnswer)
            .filter(UserAnswer.user_id == user_id)
            .order_by(desc(UserAnswer.answered_at))
            .limit(50)
            .all()
        ]
        
        # Se tem tópicos fracos, focar neles
        if analysis.get("weak_topics"):
            weak_topic = analysis["weak_topics"][0]
            
            questions = self.db.query(Question).filter(
                Question.disciplina == weak_topic["disciplina"],
                Question.topico == weak_topic["topico"],
                ~Question.id.in_(answered_ids)
            ).limit(quantity).all()
            
            if questions:
                return questions
        
        # Caso contrário, retornar questões variadas
        questions = self.db.query(Question).filter(
            ~Question.id.in_(answered_ids)
        ).order_by(func.random()).limit(quantity).all()
        
        return questions
    
    def predict_exam_performance(self, user_id: int) -> Dict:
        """
        Prevê o desempenho do usuário em uma prova real
        baseado no histórico de respostas
        """
        
        analysis = self.analyze_user_performance(user_id)
        
        if analysis["status"] == "insufficient_data":
            return {
                "status": "insufficient_data",
                "message": "Dados insuficientes para previsão"
            }
        
        overall_acc = analysis["overall_accuracy"]
        
        # Calcular nota estimada (0-100)
        estimated_score = overall_acc
        
        # Ajustar baseado no padrão de aprendizado
        pattern = analysis["learning_pattern"]
        if pattern == "improving":
            estimated_score += 5
        elif pattern == "declining":
            estimated_score -= 5
        
        # Calcular probabilidade de aprovação (assumindo nota mínima 60)
        if estimated_score >= 70:
            approval_probability = 85
            status = "excellent"
        elif estimated_score >= 60:
            approval_probability = 70
            status = "good"
        elif estimated_score >= 50:
            approval_probability = 50
            status = "borderline"
        else:
            approval_probability = 30
            status = "needs_improvement"
        
        return {
            "status": "success",
            "estimated_score": round(estimated_score, 1),
            "approval_probability": approval_probability,
            "performance_status": status,
            "weak_areas": len(analysis["weak_topics"]),
            "strong_areas": len(analysis["strong_topics"]),
            "recommendation": self._get_recommendation(status, analysis)
        }
    
    def _get_recommendation(self, status: str, analysis: Dict) -> str:
        """Gera recomendação baseada no status"""
        
        if status == "excellent":
            return "Você está muito bem! Continue praticando e foque em manter a consistência."
        elif status == "good":
            return f"Bom desempenho! Foque em melhorar: {', '.join([t['topico'] for t in analysis['weak_topics'][:2]])}"
        elif status == "borderline":
            return f"Você está no limite. URGENTE: estude mais {', '.join([t['topico'] for t in analysis['weak_topics'][:3]])}"
        else:
            return "Precisa melhorar bastante. Recomendo fazer 2-3 provas completas por semana e focar nos pontos fracos."
