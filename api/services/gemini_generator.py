import logging
import os
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import Question, Topic, DifficultyLevel, QAStatus
from services.qa_validator import QAValidator
from services.rate_limiter import gemini_rate_limiter

logger = logging.getLogger(__name__)

class GeminiQuestionGenerator:
    """
    Gerador de questões usando Gemini Pro.
    Gera questões realistas baseadas em exemplos de provas reais.
    """
    
    def __init__(self, db: Session, api_key: Optional[str] = None):
        self.db = db
        self.validator = QAValidator()
        
        # Configurar Gemini
        api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY não configurada")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_questions_with_ai(
        self,
        topic: Topic,
        quantity: int = 10,
        reference_questions: List[Dict] = None,
        difficulty: Optional[DifficultyLevel] = None
    ) -> List[Question]:
        """
        Gera questões usando Gemini Pro baseadas em exemplos reais.
        """
        generated = []
        
        # Criar prompt com exemplos
        prompt = self._build_prompt(topic, quantity, reference_questions, difficulty)
        
        try:
            # Verificar rate limit
            can_make, error_msg = gemini_rate_limiter.can_make_request()
            if not can_make:
                logger.error(f"Rate limit exceeded: {error_msg}")
                raise HTTPException(status_code=429, detail=error_msg)
            
            # Gerar com Gemini
            response = self.model.generate_content(prompt)
            
            # Registrar requisição
            gemini_rate_limiter.record_request()
            
            # Parsear resposta
            questions_data = self._parse_gemini_response(response.text, topic)
            
            # Validar e salvar
            for q_data in questions_data:
                question = self._validate_and_save(q_data)
                if question:
                    generated.append(question)
            
            logger.info(f"Generated {len(generated)} questions with Gemini for topic {topic.id}")
            
        except Exception as e:
            logger.error(f"Error generating with Gemini: {str(e)}")
        
        return generated
    
    def _build_prompt(
        self,
        topic: Topic,
        quantity: int,
        reference_questions: List[Dict],
        difficulty: Optional[DifficultyLevel]
    ) -> str:
        """Constrói prompt para o Gemini"""
        
        prompt = f"""Você é um especialista em criar questões de concurso público para o cargo de Técnico em Informática.

TAREFA: Gerar {quantity} questões de múltipla escolha sobre o tema "{topic.topico}" da disciplina "{topic.disciplina}".

CARACTERÍSTICAS DAS QUESTÕES:
- Estilo: Concurso público (IBGP, CESPE, FCC)
- Nível: {"Fácil" if difficulty == DifficultyLevel.FACIL else "Médio" if difficulty == DifficultyLevel.MEDIO else "Difícil" if difficulty else "Variado"}
- 4 alternativas (A, B, C, D)
- Apenas 1 alternativa correta
- Distratores plausíveis (alternativas erradas que parecem corretas)
- Enunciado claro e objetivo
- Explicação detalhada da resposta

"""
        
        # Adicionar exemplos de questões reais
        if reference_questions:
            prompt += "\nEXEMPLOS DE QUESTÕES REAIS (use como referência de estilo):\n\n"
            for i, ref in enumerate(reference_questions[:3], 1):
                prompt += f"EXEMPLO {i}:\n"
                prompt += f"Enunciado: {ref.get('enunciado', '')}\n"
                prompt += f"A) {ref.get('alternativa_a', '')}\n"
                prompt += f"B) {ref.get('alternativa_b', '')}\n"
                prompt += f"C) {ref.get('alternativa_c', '')}\n"
                prompt += f"D) {ref.get('alternativa_d', '')}\n"
                prompt += f"Gabarito: {ref.get('gabarito', '')}\n"
                prompt += f"Explicação: {ref.get('explicacao_detalhada', '')}\n\n"
        
        prompt += """
FORMATO DE SAÍDA (para cada questão):
---QUESTAO---
ENUNCIADO: [texto do enunciado]
A) [alternativa A]
B) [alternativa B]
C) [alternativa C]
D) [alternativa D]
GABARITO: [A, B, C ou D]
EXPLICACAO: [explicação detalhada da resposta correta]
DIFICULDADE: [FACIL, MEDIO ou DIFICIL]
TEMPO_ESTIMADO: [tempo em minutos: 1-6]
---FIM---

Gere as questões agora:
"""
        
        return prompt
    
    def _parse_gemini_response(self, response_text: str, topic: Topic) -> List[Dict[str, Any]]:
        """Parseia resposta do Gemini em formato estruturado"""
        questions = []
        
        # Dividir por questões
        parts = response_text.split('---QUESTAO---')
        
        for part in parts:
            if '---FIM---' not in part:
                continue
            
            try:
                # Extrair campos
                question_data = {
                    'topic_id': topic.id,
                    'disciplina': topic.disciplina,
                    'topico': topic.topico,
                    'subtopico': topic.subtopico,
                    'referencia': topic.reference,
                    'keywords': [topic.disciplina, topic.topico],
                    'qa_status': QAStatus.APPROVED
                }
                
                # Enunciado
                if 'ENUNCIADO:' in part:
                    enunciado = part.split('ENUNCIADO:')[1].split('A)')[0].strip()
                    question_data['enunciado'] = enunciado
                
                # Alternativas
                for letter in ['A', 'B', 'C', 'D']:
                    next_letter = chr(ord(letter) + 1) if letter != 'D' else 'GABARITO'
                    if f'{letter})' in part:
                        alt_text = part.split(f'{letter})')[1].split(f'{next_letter}')[0].strip()
                        question_data[f'alternativa_{letter.lower()}'] = alt_text
                
                # Gabarito
                if 'GABARITO:' in part:
                    gabarito = part.split('GABARITO:')[1].split('\n')[0].strip()
                    question_data['gabarito'] = gabarito.upper()
                
                # Explicação
                if 'EXPLICACAO:' in part:
                    explicacao = part.split('EXPLICACAO:')[1].split('DIFICULDADE:')[0].strip()
                    question_data['explicacao_detalhada'] = explicacao
                
                # Dificuldade
                if 'DIFICULDADE:' in part:
                    dif_text = part.split('DIFICULDADE:')[1].split('\n')[0].strip().upper()
                    if 'FACIL' in dif_text:
                        question_data['dificuldade'] = DifficultyLevel.FACIL
                    elif 'DIFICIL' in dif_text:
                        question_data['dificuldade'] = DifficultyLevel.DIFICIL
                    else:
                        question_data['dificuldade'] = DifficultyLevel.MEDIO
                
                # Tempo estimado
                if 'TEMPO_ESTIMADO:' in part:
                    tempo_text = part.split('TEMPO_ESTIMADO:')[1].split('\n')[0].strip()
                    try:
                        question_data['estimativa_tempo'] = int(''.join(filter(str.isdigit, tempo_text)))
                    except:
                        question_data['estimativa_tempo'] = 3
                
                # Validar campos obrigatórios
                required = ['enunciado', 'alternativa_a', 'alternativa_b', 'alternativa_c', 'alternativa_d', 'gabarito']
                if all(field in question_data for field in required):
                    questions.append(question_data)
                
            except Exception as e:
                logger.error(f"Error parsing question: {str(e)}")
                continue
        
        return questions
    
    def _validate_and_save(self, question_data: Dict[str, Any]) -> Optional[Question]:
        """Valida e salva questão no banco"""
        try:
            # Validação QA
            qa_result = self.validator.validate(question_data)
            question_data['qa_score'] = qa_result['score']
            question_data['qa_status'] = qa_result['status']
            
            # Só salvar se aprovada
            if qa_result['status'] == QAStatus.REJECTED:
                logger.warning(f"Question rejected by QA: {qa_result['issues']}")
                return None
            
            # Salvar
            question = Question(**question_data)
            self.db.add(question)
            self.db.commit()
            self.db.refresh(question)
            
            return question
            
        except Exception as e:
            logger.error(f"Error saving question: {str(e)}")
            self.db.rollback()
            return None
    
    def improve_existing_question(self, question: Question) -> Optional[Question]:
        """Melhora uma questão existente usando Gemini"""
        
        prompt = f"""Você é um especialista em questões de concurso. Melhore a seguinte questão:

QUESTÃO ATUAL:
Enunciado: {question.enunciado}
A) {question.alternativa_a}
B) {question.alternativa_b}
C) {question.alternativa_c}
D) {question.alternativa_d}
Gabarito: {question.gabarito}

MELHORIAS NECESSÁRIAS:
1. Tornar o enunciado mais claro e objetivo
2. Melhorar os distratores (alternativas erradas mais plausíveis)
3. Adicionar contexto técnico realista
4. Garantir que apenas uma alternativa está correta

Retorne a questão melhorada no mesmo formato.
"""
        
        try:
            # Verificar rate limit
            can_make, error_msg = gemini_rate_limiter.can_make_request()
            if not can_make:
                logger.error(f"Rate limit exceeded: {error_msg}")
                raise HTTPException(status_code=429, detail=error_msg)
            
            response = self.model.generate_content(prompt)
            
            # Registrar requisição
            gemini_rate_limiter.record_request()
            
            improved_data = self._parse_gemini_response(response.text, question.topic)
            
            if improved_data:
                # Atualizar questão existente
                for key, value in improved_data[0].items():
                    if hasattr(question, key):
                        setattr(question, key, value)
                
                self.db.commit()
                return question
                
        except Exception as e:
            logger.error(f"Error improving question: {str(e)}")
        
        return None
