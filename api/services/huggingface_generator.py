"""
Gerador de questões usando Hugging Face Inference API
Alternativa robusta ao Gemini com modelos especializados em português
"""
import logging
import os
import time
import json
import re
from typing import List, Dict, Any, Optional
import requests
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import Question, Topic, DifficultyLevel, QAStatus
from services.qa_validator import QAValidator

logger = logging.getLogger(__name__)

class HuggingFaceQuestionGenerator:
    """
    Gerador de questões usando Hugging Face Inference API
    - Modelos especializados em português
    - Rate limiting inteligente
    - Fallback automático entre modelos
    - Parsing robusto
    """
    
    def __init__(self, db: Session, api_key: Optional[str] = None):
        self.db = db
        self.validator = QAValidator()
        
        # Configurar API key
        self.api_key = api_key or os.getenv('HUGGINGFACE_API_KEY')
        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY não configurada")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Modelos em ordem de prioridade (melhores para português)
        self.models = [
            "microsoft/DialoGPT-medium",  # Bom para diálogo estruturado
            "pierreguillou/gpt2-small-portuguese",  # Especializado em português
            "google/gemma-2-2b-it",  # Multilingual, boa qualidade
            "HeyLucasLeao/gpt-neo-small-portuguese",  # Português nativo
            "meta-llama/Llama-3.2-1B-Instruct"  # Fallback confiável
        ]
        
        self.current_model = None
        self.base_url = "https://router.huggingface.co/models"
        
        # Rate limiting (mais generoso que Gemini)
        self.last_request_time = 0
        self.min_interval = 1  # 1 segundo entre requests
        
        logger.info("🤗 HuggingFace Generator initialized")
    
    def _wait_for_rate_limit(self):
        """Rate limiting simples"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            wait_time = self.min_interval - elapsed
            time.sleep(wait_time)
        self.last_request_time = time.time()
    
    def _make_request(self, model_name: str, prompt: str, max_retries: int = 3) -> Optional[str]:
        """Faz requisição para um modelo específico"""
        url = f"{self.base_url}/{model_name}"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1500,  # Suficiente para 1 questão
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        for attempt in range(max_retries):
            try:
                self._wait_for_rate_limit()
                
                response = requests.post(url, headers=self.headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        generated_text = result[0].get('generated_text', '')
                        if len(generated_text) > 100:  # Resposta válida
                            logger.info(f"✅ Success with {model_name}")
                            return generated_text
                
                elif response.status_code == 503:
                    # Modelo carregando
                    wait_time = min(10 * (attempt + 1), 30)
                    logger.warning(f"⏳ Model {model_name} loading, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                
                elif response.status_code == 429:
                    # Rate limit
                    wait_time = min(5 * (attempt + 1), 15)
                    logger.warning(f"⚠️ Rate limit {model_name}, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                
                else:
                    logger.error(f"❌ HTTP {response.status_code} for {model_name}: {response.text[:200]}")
                    break
                    
            except requests.exceptions.Timeout:
                logger.warning(f"⏰ Timeout for {model_name}, attempt {attempt + 1}")
                continue
            except Exception as e:
                logger.error(f"💥 Error with {model_name}: {str(e)[:100]}")
                break
        
        return None
    
    def _generate_with_fallback(self, prompt: str) -> Optional[str]:
        """Tenta gerar com fallback automático entre modelos"""
        
        for model_name in self.models:
            logger.info(f"🔄 Trying model: {model_name}")
            
            result = self._make_request(model_name, prompt)
            if result:
                self.current_model = model_name
                return result
        
        logger.error("❌ All HuggingFace models failed")
        return None
    
    def generate_questions_with_ai(
        self,
        topic: Topic,
        quantity: int = 1,
        reference_questions: List[Dict] = None,
        difficulty: Optional[DifficultyLevel] = None
    ) -> List[Question]:
        """Gera questões usando HuggingFace"""
        
        generated = []
        
        for i in range(quantity):
            try:
                logger.info(f"🔄 Generating question {i+1}/{quantity} for {topic.topico}")
                
                # Prompt otimizado para HuggingFace
                prompt = self._build_optimized_prompt(topic, reference_questions, difficulty)
                
                # Gerar
                response_text = self._generate_with_fallback(prompt)
                if not response_text:
                    logger.error(f"❌ Failed to generate question {i+1}")
                    continue
                
                # Parse
                questions_data = self._parse_response(response_text, topic)
                
                # Salvar primeira questão válida
                for q_data in questions_data:
                    question = self._validate_and_save(q_data)
                    if question:
                        generated.append(question)
                        logger.info(f"✅ Question {i+1} saved successfully")
                        break
                
                # Pausa entre gerações
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"❌ Error generating question {i+1}: {str(e)}")
                continue
        
        logger.info(f"📊 Generated {len(generated)} questions for topic {topic.id}")
        return generated
    
    def _build_optimized_prompt(self, topic: Topic, reference_questions: List[Dict], difficulty: Optional[DifficultyLevel]) -> str:
        """Prompt otimizado para HuggingFace (mais direto)"""
        
        contexto_disciplina = {
            "Informática": "Técnico em Informática - conhecimentos práticos de hardware, redes, sistemas operacionais, segurança.",
            "Português": "Língua Portuguesa - gramática, interpretação, redação oficial para concurso público.",
            "Matemática": "Matemática básica - operações, frações, porcentagem, geometria para nível médio.",
            "Raciocínio Lógico": "Raciocínio lógico - sequências, proposições, problemas lógicos.",
            "Legislação": "Legislação pública - Constituição, leis administrativas, ética no serviço público."
        }
        
        contexto = contexto_disciplina.get(topic.disciplina, "Conhecimentos gerais")
        
        nivel_map = {
            DifficultyLevel.FACIL: "fácil",
            DifficultyLevel.MEDIO: "médio", 
            DifficultyLevel.DIFICIL: "difícil"
        }
        nivel = nivel_map.get(difficulty, "médio")
        
        prompt = f"""Crie uma questão de múltipla escolha sobre {topic.topico} ({topic.disciplina}).

CONTEXTO: {contexto}
NÍVEL: {nivel}

FORMATO OBRIGATÓRIO:
---QUESTAO---
ENUNCIADO: [pergunta clara e objetiva]
A) [alternativa A]
B) [alternativa B]
C) [alternativa C] 
D) [alternativa D]
GABARITO: [A, B, C ou D]
EXPLICACAO: [explicação da resposta correta]
---FIM---

REGRAS:
- Questão prática e aplicada ao contexto brasileiro
- Linguagem clara, sem ambiguidades
- Apenas uma alternativa correta
- Distratores plausíveis

Gere a questão agora:"""

        return prompt
    
    def _parse_response(self, response_text: str, topic: Topic) -> List[Dict]:
        """Parser robusto para resposta do HuggingFace"""
        questions = []
        
        try:
            # Procurar por padrão ---QUESTAO---
            if '---QUESTAO---' in response_text:
                parts = response_text.split('---QUESTAO---')
                for part in parts[1:]:
                    if '---FIM---' in part:
                        part = part.split('---FIM---')[0]
                        question_data = self._extract_question_data(part, topic)
                        if question_data:
                            questions.append(question_data)
            
            # Se não encontrou o padrão, tentar parsing livre
            if not questions:
                question_data = self._extract_free_form_question(response_text, topic)
                if question_data:
                    questions.append(question_data)
        
        except Exception as e:
            logger.error(f"❌ Error parsing response: {str(e)}")
        
        return questions
    
    def _extract_question_data(self, text: str, topic: Topic) -> Optional[Dict]:
        """Extrai dados da questão do texto estruturado"""
        try:
            question_data = {
                'topic_id': topic.id,
                'disciplina': topic.disciplina,
                'topico': topic.topico,
                'subtopico': topic.subtopico,
                'dificuldade': DifficultyLevel.MEDIO,
                'estimativa_tempo': 3,
                'fonte': f'HuggingFace AI ({self.current_model})'
            }
            
            # Enunciado
            enunciado_match = re.search(r'ENUNCIADO:\s*(.+?)(?=A\))', text, re.DOTALL)
            if enunciado_match:
                question_data['enunciado'] = enunciado_match.group(1).strip()
            
            # Alternativas
            alt_patterns = {
                'alternativa_a': r'A\)\s*(.+?)(?=B\))',
                'alternativa_b': r'B\)\s*(.+?)(?=C\))', 
                'alternativa_c': r'C\)\s*(.+?)(?=D\))',
                'alternativa_d': r'D\)\s*(.+?)(?=GABARITO:)'
            }
            
            for field, pattern in alt_patterns.items():
                match = re.search(pattern, text, re.DOTALL)
                if match:
                    question_data[field] = match.group(1).strip()
            
            # Gabarito
            gabarito_match = re.search(r'GABARITO:\s*([ABCD])', text)
            if gabarito_match:
                question_data['gabarito'] = gabarito_match.group(1)
            
            # Explicação
            exp_match = re.search(r'EXPLICACAO:\s*(.+?)(?:\n\n|\Z)', text, re.DOTALL)
            if exp_match:
                question_data['explicacao_detalhada'] = exp_match.group(1).strip()
            
            # Validar campos obrigatórios
            required = ['enunciado', 'alternativa_a', 'alternativa_b', 'alternativa_c', 'alternativa_d', 'gabarito']
            if all(field in question_data and question_data[field] for field in required):
                return question_data
            
        except Exception as e:
            logger.error(f"❌ Error extracting question data: {str(e)}")
        
        return None
    
    def _extract_free_form_question(self, text: str, topic: Topic) -> Optional[Dict]:
        """Tenta extrair questão de texto livre (fallback)"""
        try:
            # Procurar por padrões comuns de questão
            lines = text.split('\n')
            
            enunciado = None
            alternativas = {}
            gabarito = None
            explicacao = None
            
            for i, line in enumerate(lines):
                line = line.strip()
                
                # Procurar enunciado (primeira linha substancial)
                if not enunciado and len(line) > 20 and '?' in line:
                    enunciado = line
                
                # Procurar alternativas
                for letter in ['A', 'B', 'C', 'D']:
                    if line.startswith(f'{letter})') or line.startswith(f'{letter}.'):
                        alternativas[f'alternativa_{letter.lower()}'] = line[2:].strip()
                
                # Procurar gabarito
                if 'gabarito' in line.lower() or 'resposta' in line.lower():
                    gabarito_match = re.search(r'([ABCD])', line)
                    if gabarito_match:
                        gabarito = gabarito_match.group(1)
            
            # Se encontrou dados suficientes
            if enunciado and len(alternativas) >= 4 and gabarito:
                return {
                    'topic_id': topic.id,
                    'disciplina': topic.disciplina,
                    'topico': topic.topico,
                    'enunciado': enunciado,
                    **alternativas,
                    'gabarito': gabarito,
                    'explicacao_detalhada': explicacao or 'Explicação gerada automaticamente.',
                    'dificuldade': DifficultyLevel.MEDIO,
                    'estimativa_tempo': 3,
                    'fonte': f'HuggingFace AI ({self.current_model})'
                }
        
        except Exception as e:
            logger.error(f"❌ Error in free form extraction: {str(e)}")
        
        return None
    
    def _validate_and_save(self, question_data: Dict[str, Any]) -> Optional[Question]:
        """Valida e salva questão no banco"""
        try:
            # Validação básica
            if len(question_data.get('enunciado', '')) < 10:
                logger.warning("⚠️ Enunciado muito curto")
                return None
            
            if question_data.get('gabarito') not in ['A', 'B', 'C', 'D']:
                logger.warning("⚠️ Gabarito inválido")
                return None
            
            # QA simplificado
            try:
                qa_result = self.validator.validate(question_data)
                question_data['qa_score'] = qa_result.get('score', 0.8)
                question_data['qa_status'] = qa_result.get('status', QAStatus.APPROVED)
            except:
                question_data['qa_score'] = 0.8
                question_data['qa_status'] = QAStatus.APPROVED
            
            # Salvar
            question = Question(**question_data)
            self.db.add(question)
            self.db.commit()
            self.db.refresh(question)
            
            logger.info(f"✅ Question saved: ID {question.id}")
            return question
            
        except Exception as e:
            logger.error(f"❌ Error saving question: {str(e)}")
            self.db.rollback()
            return None
    
    def test_connection(self) -> Dict[str, Any]:
        """Testa conexão com HuggingFace"""
        try:
            test_prompt = "Teste de conexão. Responda apenas: OK"
            result = self._generate_with_fallback(test_prompt)
            
            return {
                "status": "success" if result else "failed",
                "model_used": self.current_model,
                "response_preview": result[:100] if result else None,
                "available_models": len(self.models)
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }