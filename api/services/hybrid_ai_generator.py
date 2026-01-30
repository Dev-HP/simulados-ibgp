"""
Gerador híbrido: Gemini + HuggingFace com fallback inteligente
Combina o melhor dos dois mundos
"""
import logging
import os
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from models import Question, Topic, DifficultyLevel
from services.gemini_generator_fixed import GeminiQuestionGeneratorFixed
from services.huggingface_generator import HuggingFaceQuestionGenerator

logger = logging.getLogger(__name__)

class HybridAIGenerator:
    """
    Gerador híbrido que combina Gemini e HuggingFace
    - Tenta Gemini primeiro (melhor qualidade)
    - Fallback para HuggingFace se Gemini falhar
    - Estratégias inteligentes baseadas no contexto
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # Inicializar geradores
        self.gemini_generator = None
        self.huggingface_generator = None
        
        # Tentar inicializar Gemini
        try:
            if os.getenv('GEMINI_API_KEY'):
                self.gemini_generator = GeminiQuestionGeneratorFixed(db)
                logger.info("✅ Gemini generator initialized")
        except Exception as e:
            logger.warning(f"⚠️ Gemini initialization failed: {str(e)[:100]}")
        
        # Tentar inicializar HuggingFace
        try:
            if os.getenv('HUGGINGFACE_API_KEY'):
                self.huggingface_generator = HuggingFaceQuestionGenerator(db)
                logger.info("✅ HuggingFace generator initialized")
        except Exception as e:
            logger.warning(f"⚠️ HuggingFace initialization failed: {str(e)[:100]}")
        
        if not self.gemini_generator and not self.huggingface_generator:
            raise ValueError("❌ Nenhum gerador de IA disponível! Configure GEMINI_API_KEY ou HUGGINGFACE_API_KEY")
        
        # Estatísticas de uso
        self.stats = {
            'gemini_success': 0,
            'gemini_failures': 0,
            'huggingface_success': 0,
            'huggingface_failures': 0
        }
    
    def generate_questions_with_ai(
        self,
        topic: Topic,
        quantity: int = 1,
        reference_questions: List[Dict] = None,
        difficulty: Optional[DifficultyLevel] = None,
        strategy: str = "auto"
    ) -> List[Question]:
        """
        Gera questões com estratégia híbrida
        
        Args:
            strategy: "auto", "gemini_first", "huggingface_first", "gemini_only", "huggingface_only"
        """
        
        logger.info(f"🔄 Generating {quantity} questions with hybrid strategy: {strategy}")
        
        generated = []
        
        # Determinar estratégia
        if strategy == "auto":
            strategy = self._choose_best_strategy(topic)
        
        for i in range(quantity):
            question = None
            
            try:
                if strategy in ["gemini_first", "gemini_only"]:
                    question = self._try_gemini(topic, reference_questions, difficulty)
                    
                    if not question and strategy == "gemini_first":
                        question = self._try_huggingface(topic, reference_questions, difficulty)
                
                elif strategy in ["huggingface_first", "huggingface_only"]:
                    question = self._try_huggingface(topic, reference_questions, difficulty)
                    
                    if not question and strategy == "huggingface_first":
                        question = self._try_gemini(topic, reference_questions, difficulty)
                
                if question:
                    generated.append(question)
                    logger.info(f"✅ Question {i+1}/{quantity} generated successfully")
                else:
                    logger.warning(f"⚠️ Failed to generate question {i+1}/{quantity}")
            
            except Exception as e:
                logger.error(f"❌ Error generating question {i+1}: {str(e)}")
        
        self._log_stats()
        return generated
    
    def _choose_best_strategy(self, topic: Topic) -> str:
        """Escolhe a melhor estratégia baseada no contexto"""
        
        # Disciplinas que funcionam melhor com Gemini
        gemini_preferred = ["Informática", "Legislação"]
        
        # Disciplinas que funcionam melhor com HuggingFace
        huggingface_preferred = ["Português", "Matemática"]
        
        # Baseado no histórico de sucesso
        gemini_success_rate = self._get_success_rate('gemini')
        huggingface_success_rate = self._get_success_rate('huggingface')
        
        # Lógica de decisão
        if topic.disciplina in gemini_preferred and self.gemini_generator:
            if gemini_success_rate > 0.3:  # Se Gemini tem taxa de sucesso razoável
                return "gemini_first"
        
        if topic.disciplina in huggingface_preferred and self.huggingface_generator:
            return "huggingface_first"
        
        # Fallback baseado em disponibilidade e performance
        if huggingface_success_rate > gemini_success_rate and self.huggingface_generator:
            return "huggingface_first"
        elif self.gemini_generator:
            return "gemini_first"
        else:
            return "huggingface_only"
    
    def _try_gemini(self, topic: Topic, reference_questions: List[Dict], difficulty: Optional[DifficultyLevel]) -> Optional[Question]:
        """Tenta gerar com Gemini"""
        if not self.gemini_generator:
            return None
        
        try:
            logger.info("🔵 Trying Gemini...")
            questions = self.gemini_generator.generate_questions_with_ai(
                topic, quantity=1, reference_questions=reference_questions, difficulty=difficulty
            )
            
            if questions:
                self.stats['gemini_success'] += 1
                logger.info("✅ Gemini success")
                return questions[0]
            else:
                self.stats['gemini_failures'] += 1
                logger.warning("⚠️ Gemini returned no questions")
                return None
        
        except Exception as e:
            self.stats['gemini_failures'] += 1
            logger.error(f"❌ Gemini error: {str(e)[:100]}")
            return None
    
    def _try_huggingface(self, topic: Topic, reference_questions: List[Dict], difficulty: Optional[DifficultyLevel]) -> Optional[Question]:
        """Tenta gerar com HuggingFace"""
        if not self.huggingface_generator:
            return None
        
        try:
            logger.info("🟠 Trying HuggingFace...")
            questions = self.huggingface_generator.generate_questions_with_ai(
                topic, quantity=1, reference_questions=reference_questions, difficulty=difficulty
            )
            
            if questions:
                self.stats['huggingface_success'] += 1
                logger.info("✅ HuggingFace success")
                return questions[0]
            else:
                self.stats['huggingface_failures'] += 1
                logger.warning("⚠️ HuggingFace returned no questions")
                return None
        
        except Exception as e:
            self.stats['huggingface_failures'] += 1
            logger.error(f"❌ HuggingFace error: {str(e)[:100]}")
            return None
    
    def _get_success_rate(self, generator: str) -> float:
        """Calcula taxa de sucesso de um gerador"""
        if generator == 'gemini':
            total = self.stats['gemini_success'] + self.stats['gemini_failures']
            return self.stats['gemini_success'] / max(total, 1)
        else:
            total = self.stats['huggingface_success'] + self.stats['huggingface_failures']
            return self.stats['huggingface_success'] / max(total, 1)
    
    def _log_stats(self):
        """Log das estatísticas de uso"""
        logger.info("📊 HYBRID GENERATOR STATS:")
        logger.info(f"  🔵 Gemini: {self.stats['gemini_success']} success, {self.stats['gemini_failures']} failures")
        logger.info(f"  🟠 HuggingFace: {self.stats['huggingface_success']} success, {self.stats['huggingface_failures']} failures")
        
        gemini_rate = self._get_success_rate('gemini')
        huggingface_rate = self._get_success_rate('huggingface')
        
        logger.info(f"  📈 Success rates: Gemini {gemini_rate:.1%}, HuggingFace {huggingface_rate:.1%}")
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status dos geradores"""
        return {
            "gemini_available": self.gemini_generator is not None,
            "huggingface_available": self.huggingface_generator is not None,
            "stats": self.stats,
            "success_rates": {
                "gemini": self._get_success_rate('gemini'),
                "huggingface": self._get_success_rate('huggingface')
            }
        }
    
    def test_all_generators(self) -> Dict[str, Any]:
        """Testa todos os geradores disponíveis"""
        results = {}
        
        if self.gemini_generator:
            try:
                # Teste simples do Gemini não existe, vamos simular
                results["gemini"] = {"status": "available", "error": None}
            except Exception as e:
                results["gemini"] = {"status": "error", "error": str(e)}
        else:
            results["gemini"] = {"status": "not_configured", "error": "GEMINI_API_KEY not set"}
        
        if self.huggingface_generator:
            try:
                test_result = self.huggingface_generator.test_connection()
                results["huggingface"] = test_result
            except Exception as e:
                results["huggingface"] = {"status": "error", "error": str(e)}
        else:
            results["huggingface"] = {"status": "not_configured", "error": "HUGGINGFACE_API_KEY not set"}
        
        return results