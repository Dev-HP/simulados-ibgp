#!/usr/bin/env python3
"""
Script de seed para popular banco com dados de amostra.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, engine, Base
from models import User, Syllabus, Topic, Question, DifficultyLevel, QAStatus
from auth import get_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_database():
    """Popula banco com dados de amostra"""
    db = SessionLocal()
    
    try:
        # Criar tabelas
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created")
        
        # Criar usuário de teste
        user = User(
            email="teste@example.com",
            username="teste",
            hashed_password=get_password_hash("senha123"),
            full_name="Usuário Teste"
        )
        db.add(user)
        db.commit()
        logger.info("Test user created")
        
        # Criar syllabus de amostra
        syllabus = Syllabus(
            filename="edital_amostra.txt",
            content="Conteúdo programático de amostra",
            parsed_structure={
                "disciplinas": [
                    {"nome": "Hardware", "topicos": []},
                    {"nome": "Redes", "topicos": []},
                    {"nome": "Linux", "topicos": []}
                ]
            },
            source_reference="edital_amostra.txt"
        )
        db.add(syllabus)
        db.commit()
        logger.info("Sample syllabus created")
        
        # Criar tópicos
        topics_data = [
            ("Hardware", "Componentes de Hardware", "Memórias"),
            ("Hardware", "Periféricos", None),
            ("Redes", "Protocolos TCP/IP", "IPv4 e IPv6"),
            ("Redes", "VLAN", None),
            ("Linux", "Comandos básicos", "wc, ls, cat"),
            ("Informática", "Excel", "Funções CONT.SE")
        ]
        
        topics = []
        for disc, top, sub in topics_data:
            topic = Topic(
                syllabus_id=syllabus.id,
                disciplina=disc,
                topico=top,
                subtopico=sub,
                reference=f"Edital página 1"
            )
            db.add(topic)
            topics.append(topic)
        
        db.commit()
        logger.info(f"Created {len(topics)} topics")
        
        # Criar questões de amostra
        sample_questions = [
            {
                "topic_id": topics[0].id,
                "disciplina": "Hardware",
                "topico": "Componentes de Hardware",
                "subtopico": "Memórias",
                "enunciado": "Sobre memórias RAM, é correto afirmar que:",
                "alternativa_a": "São memórias voláteis que perdem dados ao desligar o computador",
                "alternativa_b": "São memórias permanentes como HD e SSD",
                "alternativa_c": "Não influenciam na velocidade do sistema",
                "alternativa_d": "São utilizadas apenas para armazenamento de arquivos",
                "gabarito": "A",
                "explicacao_detalhada": "A alternativa A está correta. Memórias RAM são voláteis, ou seja, perdem seu conteúdo quando o computador é desligado.",
                "referencia": "Edital - Hardware, página 2",
                "dificuldade": DifficultyLevel.FACIL,
                "estimativa_tempo": 2,
                "keywords": ["hardware", "memória", "RAM"],
                "seed": "hw_001",
                "qa_score": 95.0,
                "qa_status": QAStatus.APPROVED
            },
            {
                "topic_id": topics[2].id,
                "disciplina": "Redes",
                "topico": "Protocolos TCP/IP",
                "subtopico": "IPv4 e IPv6",
                "enunciado": "Qual a principal diferença entre IPv4 e IPv6?",
                "alternativa_a": "IPv6 usa endereços de 32 bits",
                "alternativa_b": "IPv6 usa endereços de 128 bits, permitindo mais dispositivos",
                "alternativa_c": "IPv4 é mais rápido que IPv6",
                "alternativa_d": "Não há diferença significativa",
                "gabarito": "B",
                "explicacao_detalhada": "IPv6 utiliza endereços de 128 bits, enquanto IPv4 usa 32 bits. Isso permite um número muito maior de endereços únicos.",
                "referencia": "Edital - Redes, página 5",
                "dificuldade": DifficultyLevel.MEDIO,
                "estimativa_tempo": 3,
                "keywords": ["redes", "ipv4", "ipv6"],
                "seed": "net_001",
                "qa_score": 92.0,
                "qa_status": QAStatus.APPROVED
            },
            {
                "topic_id": topics[4].id,
                "disciplina": "Linux",
                "topico": "Comandos básicos",
                "subtopico": "wc, ls, cat",
                "enunciado": "O comando 'wc -c arquivo.txt' no Linux retorna:",
                "alternativa_a": "O número de linhas do arquivo",
                "alternativa_b": "O número de palavras do arquivo",
                "alternativa_c": "O número de bytes (caracteres) do arquivo",
                "alternativa_d": "O conteúdo completo do arquivo",
                "gabarito": "C",
                "explicacao_detalhada": "O comando 'wc -c' conta o número de bytes (caracteres) em um arquivo. A opção -l conta linhas e -w conta palavras.",
                "referencia": "Edital - Linux, página 8",
                "dificuldade": DifficultyLevel.MEDIO,
                "estimativa_tempo": 2,
                "keywords": ["linux", "comando", "wc"],
                "seed": "linux_001",
                "qa_score": 90.0,
                "qa_status": QAStatus.APPROVED
            },
            {
                "topic_id": topics[5].id,
                "disciplina": "Informática",
                "topico": "Excel",
                "subtopico": "Funções CONT.SE",
                "enunciado": "No Excel, a função CONT.SE é utilizada para:",
                "alternativa_a": "Somar valores que atendem a um critério",
                "alternativa_b": "Contar células que atendem a um critério específico",
                "alternativa_c": "Calcular a média de valores",
                "alternativa_d": "Concatenar textos",
                "gabarito": "B",
                "explicacao_detalhada": "CONT.SE (ou COUNTIF em inglês) conta o número de células que atendem a um critério específico.",
                "referencia": "Edital - Informática, página 10",
                "dificuldade": DifficultyLevel.FACIL,
                "estimativa_tempo": 2,
                "keywords": ["excel", "função", "cont.se"],
                "seed": "excel_001",
                "qa_score": 88.0,
                "qa_status": QAStatus.APPROVED
            }
        ]
        
        for q_data in sample_questions:
            question = Question(**q_data)
            db.add(question)
        
        db.commit()
        logger.info(f"Created {len(sample_questions)} sample questions")
        
        logger.info("✅ Database seeded successfully!")
        
    except Exception as e:
        logger.error(f"Error seeding database: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
