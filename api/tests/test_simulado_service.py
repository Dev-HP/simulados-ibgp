import pytest
from services.simulado_service import SimuladoService
from models import Question, DifficultyLevel, QAStatus
from schemas import SimuladoCreate

def test_create_simulado(db):
    # Criar questões de teste
    for i in range(10):
        q = Question(
            disciplina="Hardware",
            topico="Memórias",
            enunciado=f"Questão {i}",
            alternativa_a="A",
            alternativa_b="B",
            alternativa_c="C",
            alternativa_d="D",
            gabarito="A",
            explicacao_detalhada="Explicação",
            dificuldade=DifficultyLevel.MEDIO,
            qa_status=QAStatus.APPROVED
        )
        db.add(q)
    db.commit()
    
    # Criar simulado
    service = SimuladoService(db)
    request = SimuladoCreate(
        nome="Teste",
        numero_questoes=5,
        tempo_total=30
    )
    
    simulado = service.create_simulado(request)
    
    assert simulado.id is not None
    assert simulado.numero_questoes == 5

def test_select_questions_by_topic(db):
    # Criar questões de diferentes tópicos
    topics = ["Memórias", "Processadores", "Redes"]
    for topic in topics:
        for i in range(5):
            q = Question(
                disciplina="Hardware",
                topico=topic,
                enunciado=f"Questão {topic} {i}",
                alternativa_a="A",
                alternativa_b="B",
                alternativa_c="C",
                alternativa_d="D",
                gabarito="A",
                explicacao_detalhada="Explicação",
                dificuldade=DifficultyLevel.MEDIO,
                qa_status=QAStatus.APPROVED
            )
            db.add(q)
    db.commit()
    
    service = SimuladoService(db)
    questions = service._select_questions(
        numero_questoes=9,
        aleatorizacao_por_topico=True
    )
    
    # Deve ter questões de diferentes tópicos
    assert len(questions) == 9
    topics_in_result = set(q.topico for q in questions)
    assert len(topics_in_result) >= 2
