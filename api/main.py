from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from database import engine, get_db, Base
from routers import syllabus, questions, simulados, users, analytics, export
from models import User
from auth import get_current_user

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Simulados IBGP",
    description="API para simulados adaptativos - Técnico em Informática",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(syllabus.router, prefix="/api", tags=["Syllabus"])
app.include_router(questions.router, prefix="/api", tags=["Questions"])
app.include_router(simulados.router, prefix="/api", tags=["Simulados"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])
app.include_router(export.router, prefix="/api", tags=["Export"])

@app.get("/")
async def root():
    return {
        "message": "Sistema de Simulados IBGP - API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/seed-database")
@app.post("/api/seed-database")
async def seed_database_endpoint(db: Session = Depends(get_db)):
    """
    Endpoint para popular o banco de dados com dados de amostra.
    ATENÇÃO: Use apenas uma vez para inicializar o sistema!
    """
    try:
        from models import User, Syllabus, Topic, Question, DifficultyLevel, QAStatus
        from auth import get_password_hash
        
        # Verificar se já existe usuário
        existing_user = db.query(User).filter(User.username == "teste").first()
        if existing_user:
            return {
                "status": "already_seeded",
                "message": "Banco de dados já foi populado anteriormente"
            }
        
        # Criar usuário de teste
        user = User(
            email="teste@example.com",
            username="teste",
            hashed_password=get_password_hash("senha123"),
            full_name="Usuário Teste"
        )
        db.add(user)
        db.commit()
        
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
        db.refresh(topics[0])
        db.refresh(topics[2])
        db.refresh(topics[4])
        db.refresh(topics[5])
        
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
        
        return {
            "status": "success",
            "message": "Banco de dados populado com sucesso!",
            "data": {
                "users": 1,
                "syllabus": 1,
                "topics": len(topics),
                "questions": len(sample_questions)
            },
            "credentials": {
                "username": "teste",
                "password": "senha123"
            }
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao popular banco de dados: {str(e)}"
        )
