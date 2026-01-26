import logging
import random
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from models import (
    Simulado, SimuladoQuestion, SimuladoResult, UserAnswer,
    Question, DifficultyLevel, QAStatus
)
from schemas import SimuladoCreate, AnswerFeedback

logger = logging.getLogger(__name__)

class SimuladoService:
    """
    Serviço de criação e gerenciamento de simulados.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_simulado(self, request: SimuladoCreate) -> Simulado:
        """
        Cria simulado configurável.
        Parâmetros: numero_questoes, disciplinas, tempo_total, pesos, aleatorizacao_por_topico, dificuldade_alvo
        """
        # Buscar questões
        questions = self._select_questions(
            numero_questoes=request.numero_questoes,
            disciplinas=request.disciplinas,
            dificuldade_alvo=request.dificuldade_alvo,
            pesos=request.pesos,
            aleatorizacao_por_topico=request.aleatorizacao_por_topico
        )
        
        if len(questions) < request.numero_questoes:
            logger.warning(f"Only {len(questions)} questions available, requested {request.numero_questoes}")
        
        # Criar simulado
        simulado = Simulado(
            nome=request.nome,
            descricao=request.descricao,
            numero_questoes=len(questions),
            tempo_total=request.tempo_total,
            disciplinas=request.disciplinas,
            dificuldade_alvo=request.dificuldade_alvo,
            is_oficial=False
        )
        self.db.add(simulado)
        self.db.commit()
        self.db.refresh(simulado)
        
        # Associar questões
        for ordem, question in enumerate(questions, 1):
            sq = SimuladoQuestion(
                simulado_id=simulado.id,
                question_id=question.id,
                ordem=ordem
            )
            self.db.add(sq)
        
        self.db.commit()
        
        logger.info(f"Created simulado {simulado.id} with {len(questions)} questions")
        return simulado
    
    def _select_questions(
        self,
        numero_questoes: int,
        disciplinas: List[str] = None,
        dificuldade_alvo: str = None,
        pesos: Dict[str, float] = None,
        aleatorizacao_por_topico: bool = True
    ) -> List[Question]:
        """Seleciona questões baseado nos critérios"""
        query = self.db.query(Question).filter(
            Question.qa_status == QAStatus.APPROVED
        )
        
        # Filtrar por disciplinas
        if disciplinas:
            query = query.filter(Question.disciplina.in_(disciplinas))
        
        # Filtrar por dificuldade
        if dificuldade_alvo:
            query = query.filter(Question.dificuldade == dificuldade_alvo)
        
        # Buscar todas as questões elegíveis
        all_questions = query.all()
        
        if not all_questions:
            return []
        
        # Aleatorização por tópico
        if aleatorizacao_por_topico:
            selected = self._select_by_topic(all_questions, numero_questoes, pesos)
        else:
            selected = random.sample(all_questions, min(numero_questoes, len(all_questions)))
        
        return selected
    
    def _select_by_topic(
        self,
        questions: List[Question],
        numero_questoes: int,
        pesos: Dict[str, float] = None
    ) -> List[Question]:
        """Seleciona questões distribuídas por tópico"""
        # Agrupar por tópico
        by_topic = {}
        for q in questions:
            key = f"{q.disciplina}_{q.topico}"
            if key not in by_topic:
                by_topic[key] = []
            by_topic[key].append(q)
        
        # Calcular quantidade por tópico
        topics = list(by_topic.keys())
        questions_per_topic = numero_questoes // len(topics)
        remainder = numero_questoes % len(topics)
        
        selected = []
        for i, topic in enumerate(topics):
            topic_questions = by_topic[topic]
            
            # Aplicar peso se fornecido
            weight = pesos.get(topic, 1.0) if pesos else 1.0
            qty = int(questions_per_topic * weight)
            
            # Adicionar remainder nas primeiras
            if i < remainder:
                qty += 1
            
            # Selecionar aleatoriamente
            qty = min(qty, len(topic_questions))
            selected.extend(random.sample(topic_questions, qty))
        
        # Ajustar se necessário
        if len(selected) < numero_questoes:
            remaining = [q for q in questions if q not in selected]
            needed = numero_questoes - len(selected)
            selected.extend(random.sample(remaining, min(needed, len(remaining))))
        
        return selected[:numero_questoes]
    
    def process_answer(
        self,
        user_id: int,
        simulado_id: int,
        question_id: int,
        resposta: str,
        tempo_resposta: int = None
    ) -> AnswerFeedback:
        """
        Processa resposta e retorna feedback imediato.
        """
        # Buscar questão
        question = self.db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise ValueError("Question not found")
        
        # Verificar resposta
        is_correct = (resposta.upper() == question.gabarito.upper())
        
        # Determinar tipo de erro
        tipo_erro = None
        if not is_correct:
            tipo_erro = self._classify_error(question, resposta)
        
        # Salvar resposta
        answer = UserAnswer(
            user_id=user_id,
            question_id=question_id,
            resposta=resposta.upper(),
            is_correct=is_correct,
            tempo_resposta=tempo_resposta,
            tipo_erro=tipo_erro
        )
        self.db.add(answer)
        self.db.commit()
        
        # Buscar questões similares
        similar_questions = self._find_similar_questions(question, limit=3)
        
        return AnswerFeedback(
            is_correct=is_correct,
            gabarito=question.gabarito,
            explicacao=question.explicacao_detalhada,
            referencia=question.referencia,
            tipo_erro=tipo_erro,
            questoes_similares=[q.id for q in similar_questions]
        )
    
    def _classify_error(self, question: Question, resposta: str) -> str:
        """Classifica tipo de erro"""
        # Lógica simples de classificação
        if question.dificuldade == DifficultyLevel.FACIL:
            return "leitura"
        elif "cálculo" in question.enunciado.lower() or "calcul" in question.enunciado.lower():
            return "cálculo"
        else:
            return "conceitual"
    
    def _find_similar_questions(self, question: Question, limit: int = 3) -> List[Question]:
        """Encontra questões similares para revisão"""
        similar = self.db.query(Question).filter(
            Question.disciplina == question.disciplina,
            Question.topico == question.topico,
            Question.id != question.id,
            Question.qa_status == QAStatus.APPROVED
        ).limit(limit).all()
        
        return similar
    
    def finalize_simulado(self, user_id: int, simulado_id: int) -> SimuladoResult:
        """
        Finaliza simulado e gera relatório completo.
        """
        # Buscar respostas do usuário
        answers = self.db.query(UserAnswer).filter(
            UserAnswer.user_id == user_id
        ).join(SimuladoQuestion).filter(
            SimuladoQuestion.simulado_id == simulado_id
        ).all()
        
        if not answers:
            raise ValueError("No answers found for this simulado")
        
        # Calcular métricas
        total_questions = len(answers)
        correct_answers = sum(1 for a in answers if a.is_correct)
        score = (correct_answers / total_questions) * 100
        
        # Acertos por disciplina
        acertos_por_disciplina = self._calculate_by_discipline(answers)
        
        # Tempo médio
        tempos = [a.tempo_resposta for a in answers if a.tempo_resposta]
        tempo_medio = sum(tempos) / len(tempos) if tempos else 0
        tempo_total = sum(tempos) if tempos else None
        
        # Índice de confiança (baseado em tempo e acertos)
        indice_confianca = self._calculate_confidence(answers)
        
        # Plano de estudo
        plano_estudo = self._generate_study_plan(answers, acertos_por_disciplina)
        
        # Salvar resultado
        result = SimuladoResult(
            user_id=user_id,
            simulado_id=simulado_id,
            score=score,
            tempo_total=tempo_total,
            acertos_por_disciplina=acertos_por_disciplina,
            tempo_medio_questao=tempo_medio,
            indice_confianca=indice_confianca,
            plano_estudo=plano_estudo
        )
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)
        
        return result
    
    def _calculate_by_discipline(self, answers: List[UserAnswer]) -> Dict[str, Any]:
        """Calcula acertos por disciplina"""
        by_disc = {}
        
        for answer in answers:
            disc = answer.question.disciplina
            if disc not in by_disc:
                by_disc[disc] = {'total': 0, 'acertos': 0}
            
            by_disc[disc]['total'] += 1
            if answer.is_correct:
                by_disc[disc]['acertos'] += 1
        
        # Calcular percentuais
        for disc in by_disc:
            total = by_disc[disc]['total']
            acertos = by_disc[disc]['acertos']
            by_disc[disc]['percentual'] = (acertos / total * 100) if total > 0 else 0
        
        return by_disc
    
    def _calculate_confidence(self, answers: List[UserAnswer]) -> float:
        """Calcula índice de confiança"""
        # Baseado em: acertos + tempo adequado
        if not answers:
            return 0.0
        
        correct_count = sum(1 for a in answers if a.is_correct)
        
        # Penalizar respostas muito rápidas ou muito lentas
        adequate_time_count = 0
        for a in answers:
            if a.tempo_resposta:
                expected = a.question.estimativa_tempo * 60  # converter para segundos
                if 0.5 * expected <= a.tempo_resposta <= 2 * expected:
                    adequate_time_count += 1
        
        confidence = (correct_count * 0.7 + adequate_time_count * 0.3) / len(answers) * 100
        return confidence
    
    def _generate_study_plan(
        self,
        answers: List[UserAnswer],
        acertos_por_disciplina: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gera plano de estudo sugerido"""
        # Identificar disciplinas fracas (<60%)
        weak_disciplines = [
            disc for disc, stats in acertos_por_disciplina.items()
            if stats['percentual'] < 60
        ]
        
        # Identificar tipos de erro mais comuns
        error_types = {}
        for answer in answers:
            if not answer.is_correct and answer.tipo_erro:
                error_types[answer.tipo_erro] = error_types.get(answer.tipo_erro, 0) + 1
        
        return {
            'disciplinas_prioridade': weak_disciplines,
            'tipos_erro_comuns': error_types,
            'recomendacoes': [
                f"Revisar {disc}" for disc in weak_disciplines[:3]
            ]
        }
