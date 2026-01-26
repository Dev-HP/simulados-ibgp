import pytest
from services.parser import SyllabusParser

def test_parse_hierarchical():
    parser = SyllabusParser()
    
    content = """
HARDWARE
1. Componentes de hardware
   1.1 Memórias RAM e ROM
2. Periféricos

REDES
1. Protocolos TCP/IP
2. VLAN
"""
    
    result = parser.parse_hierarchical(content)
    
    assert 'disciplinas' in result
    assert len(result['disciplinas']) >= 2
    
    # Verificar primeira disciplina
    hardware = result['disciplinas'][0]
    assert hardware['nome'] == 'HARDWARE'
    assert len(hardware['topicos']) >= 2

def test_clean_topico():
    parser = SyllabusParser()
    
    assert parser._clean_topico('1. Componentes') == 'Componentes'
    assert parser._clean_topico('a) Memórias') == 'Memórias'
    assert parser._clean_topico('- Redes') == 'Redes'

def test_is_disciplina():
    parser = SyllabusParser()
    
    assert parser._is_disciplina('HARDWARE') == True
    assert parser._is_disciplina('Redes de Computadores') == True
    assert parser._is_disciplina('texto normal') == False
