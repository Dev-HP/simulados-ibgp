#!/usr/bin/env python3
"""
Script para validar questões existentes no banco.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models import Question, QAStatus
from services.qa_validator import QAValidator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_all_questions():
    """Valida todas as questões no banco"""
    db = SessionLocal()
    validator = QAValidator()
    
    try:
        questions = db.query(Question).all()
        logger.info(f"Validating {len(questions)} questions...")
        
        stats = {
            'approved': 0,
            'review_required': 0,
            'rejected': 0
        }
        
        for question in questions:
            q_data = {
                'enunciado': question.enunciado,
                'alternativa_a': question.alternativa_a,
                'alternativa_b': question.alternativa_b,
                'alternativa_c': question.alternativa_c,
                'alternativa_d': question.alternativa_d,
                'gabarito': question.gabarito,
                'explicacao_detalhada': question.explicacao_detalhada,
                'referencia': question.referencia
            }
            
            result = validator.validate(q_data)
            
            # Atualizar questão
            question.qa_score = result['score']
            question.qa_status = result['status']
            
            stats[result['status'].value] = stats.get(result['status'].value, 0) + 1
            
            if result['status'] == QAStatus.REVIEW_REQUIRED:
                logger.warning(f"Question {question.id} needs review: {result['issues']}")
        
        db.commit()
        
        logger.info("Validation complete!")
        logger.info(f"Approved: {stats.get('approved', 0)}")
        logger.info(f"Review Required: {stats.get('review_required', 0)}")
        logger.info(f"Rejected: {stats.get('rejected', 0)}")
        
    except Exception as e:
        logger.error(f"Error validating questions: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    validate_all_questions()
