"""
Gerador HuggingFace-only: Sistema simplificado e confiável
Usa apenas HuggingFace para máxima estabilidade
"""
import logging
import os
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from models import Question, Topic, DifficultyLevel
from services.huggingface_generator import HuggingFaceQuestionGenerator

logger = logging.getLogger(__name__)

class HybridAIGenerator:
    """
    Gerador HuggingFace-only (simplificado)
    - Usa apenas HuggingFace para máxima confiabilidade
    - Múltiplos modelos com fallback automático
    - Sistema robusto e estável
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # Inicializar apenas HuggingFace
        self.huggingface_generator = None
        
        # Tentar inicializar Groq
        try:
            if os.getenv('GROQ_API_KEY'):
                self.huggingface_generator = HuggingFaceQuestionGenerator(db)
                logger.info("✅ Groq generator initialized")
            else:
                raise ValueError("❌ GROQ_API_KEY não configurada")
        except Exception as e:
            logger.error(f"❌ Groq initialization failed: {str(e)[:100]}")
            raise ValueError("❌ Gerador Groq não disponível! Configure GROQ_API_KEY")
        
        # Estatísticas de uso (simplificadas)
        self.stats = {
            'huggingface_success': 0,
            'huggingface_failures': 0,
            'total_generated': 0
        }
    
    def generate_questions_with_ai(
        self,
        topic: Topic,
        quantity: int = 1,
        reference_questions: List[Dict] = None,
        difficulty: Optional[DifficultyLevel] = None,
        strategy: str = "huggingface_only"
    ) -> List[Question]:
        """
        Gera questões usando apenas HuggingFace
        
        Args:
            strategy: Ignorado, sempre usa "huggingface_only"
        """
        
        logger.info(f"🔄 Generating {quantity} questions with HuggingFace-only")
        
        generated = []
        
        for i in range(quantity):
            question = None
            
            try:
                question = self._try_huggingface(topic, reference_questions, difficulty)
                
                if question:
                    generated.append(question)
                    logger.info(f"✅ Question {i+1}/{quantity} generated successfully")
                else:
                    logger.warning(f"⚠️ Failed to generate question {i+1}/{quantity}")
            
            except Exception as e:
                logger.error(f"❌ Error generating question {i+1}: {str(e)}")
        
        self._log_stats()
        return generated
    
    def _try_huggingface(self, topic: Topic, reference_questions: List[Dict], difficulty: Optional[DifficultyLevel]) -> Optional[Question]:
        """Tenta gerar com HuggingFace"""
        if not self.huggingface_generator:
            logger.error("❌ HuggingFace generator not available")
            return None
        
        try:
            logger.info("🟠 Generating with HuggingFace...")
            questions = self.huggingface_generator.generate_questions_with_ai(
                topic, quantity=1, reference_questions=reference_questions, difficulty=difficulty
            )
            
            if questions:
                self.stats['huggingface_success'] += 1
                self.stats['total_generated'] += 1
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
    
    def _log_stats(self):
        """Log das estatísticas de uso"""
        logger.info("📊 HUGGINGFACE-ONLY GENERATOR STATS:")
        logger.info(f"  🟠 HuggingFace: {self.stats['huggingface_success']} success, {self.stats['huggingface_failures']} failures")
        logger.info(f"  🎯 Total generated: {self.stats['total_generated']}")
        
        success_rate = self._get_success_rate()
        logger.info(f"  📈 Success rate: {success_rate:.1%}")
    
    def _get_success_rate(self) -> float:
        """Calcula taxa de sucesso do HuggingFace"""
        total = self.stats['huggingface_success'] + self.stats['huggingface_failures']
        return self.stats['huggingface_success'] / max(total, 1)
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status do gerador (HuggingFace-only)"""
        return {
            "gemini_available": False,  # Sempre False
            "huggingface_available": self.huggingface_generator is not None,
            "stats": self.stats,
            "success_rates": {
                "gemini": 0.0,  # Sempre 0
                "huggingface": self._get_success_rate()
            },
            "mode": "huggingface_only"
        }
    
    def test_all_generators(self) -> Dict[str, Any]:
        """Testa apenas o HuggingFace"""
        results = {}
        
        # Gemini sempre indisponível
        results["gemini"] = {"status": "disabled", "error": "Gemini disabled by configuration"}
        
        # Testar HuggingFace
        if self.huggingface_generator:
            try:
                test_result = self.huggingface_generator.test_connection()
                results["huggingface"] = test_result
            except Exception as e:
                results["huggingface"] = {"status": "error", "error": str(e)}
        else:
            results["huggingface"] = {"status": "not_configured", "error": "HUGGINGFACE_API_KEY not set"}
        
        return results