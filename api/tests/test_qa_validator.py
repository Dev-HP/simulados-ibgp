import pytest
from services.qa_validator import QAValidator
from models import QAStatus

def test_validate_good_question():
    validator = QAValidator()
    
    question = {
        'enunciado': 'Sobre memórias RAM, é correto afirmar que:',
        'alternativa_a': 'São voláteis',
        'alternativa_b': 'São permanentes',
        'alternativa_c': 'Não existem',
        'alternativa_d': 'São opcionais',
        'gabarito': 'A',
        'explicacao_detalhada': 'A alternativa A está correta pois memórias RAM são voláteis.',
        'referencia': 'Edital página 1'
    }
    
    result = validator.validate(question)
    
    assert result['score'] >= 80
    assert result['status'] == QAStatus.APPROVED

def test_validate_poor_question():
    validator = QAValidator()
    
    question = {
        'enunciado': 'Teste?',
        'alternativa_a': 'A',
        'alternativa_b': 'B',
        'alternativa_c': 'C',
        'alternativa_d': 'D',
        'gabarito': 'A',
        'explicacao_detalhada': 'Curta',
        'referencia': None
    }
    
    result = validator.validate(question)
    
    assert result['score'] < 80
    assert len(result['issues']) > 0

def test_check_duplicate():
    validator = QAValidator()
    
    question = {
        'enunciado': 'Sobre memórias RAM'
    }
    
    class MockQuestion:
        enunciado = 'Sobre memórias RAM'
    
    existing = [MockQuestion()]
    
    assert validator.check_duplicate(question, existing) == True
