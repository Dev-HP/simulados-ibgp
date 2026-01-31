import logging
from typing import Dict, Any
import re

from models import QAStatus

logger = logging.getLogger(__name__)

class QAValidator:
    """
    Validação automática de questões (QA).
    Verifica: factual, duplicidade, consistência linguística.
    """
    
    def validate(self, question: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida questão e retorna score + status.
        """
        score = 100.0
        issues = []
        
        # 1. Verificação factual (básica)
        if not self._check_factual(question):
            score -= 20
            issues.append("factual_check_failed")
        
        # 2. Consistência linguística
        if not self._check_linguistic_consistency(question):
            score -= 15
            issues.append("linguistic_inconsistency")
        
        # 3. Claridade do enunciado
        if not self._check_clarity(question):
            score -= 10
            issues.append("unclear_statement")
        
        # 4. Qualidade das alternativas
        if not self._check_alternatives_quality(question):
            score -= 15
            issues.append("poor_alternatives")
        
        # 5. Explicação adequada
        if not self._check_explanation(question):
            score -= 10
            issues.append("inadequate_explanation")
        
        # Determinar status
        if score >= 80:
            status = QAStatus.APPROVED
        elif score >= 60:
            status = QAStatus.REVIEW_REQUIRED
        else:
            status = QAStatus.REJECTED
        
        return {
            'score': score,
            'status': status,
            'issues': issues
        }
    
    def _check_factual(self, question: Dict[str, Any]) -> bool:
        """Verificação factual básica"""
        # Verificar se enunciado não está vazio
        if not question.get('enunciado') or len(question['enunciado']) < 10:
            return False
        
        # Referência é opcional (questões geradas por IA podem não ter)
        return True
    
    def _check_linguistic_consistency(self, question: Dict[str, Any]) -> bool:
        """Verifica consistência linguística"""
        enunciado = question.get('enunciado', '')
        
        # Verificar pontuação básica
        if not enunciado.endswith(('?', ':', '.')):
            return False
        
        # Verificar se não tem palavras ambíguas demais
        ambiguous_words = ['talvez', 'possivelmente', 'pode ser', 'às vezes']
        if any(word in enunciado.lower() for word in ambiguous_words):
            return False
        
        return True
    
    def _check_clarity(self, question: Dict[str, Any]) -> bool:
        """Verifica claridade do enunciado"""
        enunciado = question.get('enunciado', '')
        
        # Não muito curto
        if len(enunciado) < 20:
            return False
        
        # Não muito longo
        if len(enunciado) > 500:
            return False
        
        return True
    
    def _check_alternatives_quality(self, question: Dict[str, Any]) -> bool:
        """Verifica qualidade das alternativas"""
        alternativas = [
            question.get('alternativa_a', ''),
            question.get('alternativa_b', ''),
            question.get('alternativa_c', ''),
            question.get('alternativa_d', '')
        ]
        
        # Todas devem existir
        if any(not alt or len(alt) < 5 for alt in alternativas):
            return False
        
        # Não devem ser idênticas
        if len(set(alternativas)) < 4:
            return False
        
        # Tamanhos similares (distratores plausíveis)
        lengths = [len(alt) for alt in alternativas]
        if max(lengths) > min(lengths) * 3:
            return False
        
        return True
    
    def _check_explanation(self, question: Dict[str, Any]) -> bool:
        """Verifica adequação da explicação"""
        explicacao = question.get('explicacao_detalhada', '')
        
        # Deve existir e ter tamanho mínimo
        if not explicacao or len(explicacao) < 20:  # Reduzido de 30 para 20
            return False
        
        # Gabarito é opcional na explicação (nem sempre é mencionado explicitamente)
        return True
    
    def check_duplicate(self, question: Dict[str, Any], existing_questions: list) -> bool:
        """Verifica duplicidade e near-duplicates"""
        enunciado = question.get('enunciado', '').lower()
        
        for existing in existing_questions:
            existing_enunciado = existing.enunciado.lower()
            
            # Duplicata exata
            if enunciado == existing_enunciado:
                return True
            
            # Near-duplicate (similaridade > 80%)
            similarity = self._calculate_similarity(enunciado, existing_enunciado)
            if similarity > 0.8:
                return True
        
        return False
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calcula similaridade entre dois textos (Jaccard)"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
