from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

from database import engine, get_db, Base
from routers import syllabus, questions, simulados, users, analytics, export, prova_completa
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

# CORS - Configurado para desenvolvimento e produção (Render)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Desenvolvimento local
        "http://localhost:5173",  # Vite dev server
        "https://simulados-web-porto-velho.onrender.com",  # Produção Render
        "https://*.onrender.com",  # Qualquer subdomínio do Render
    ],
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
app.include_router(prova_completa.router, prefix="/api", tags=["Prova Completa"])

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

@app.get("/api/initialize")
async def initialize_system(db: Session = Depends(get_db)):
    """
    Inicializa o sistema: cria tópicos e usuário de teste.
    Endpoint público para facilitar setup inicial.
    """
    try:
        from models import User, Topic
        from passlib.context import CryptContext
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        results = {"topics": 0, "user": "exists"}
        
        # Criar tópicos se não existirem
        topics_count = db.query(Topic).count()
        if topics_count == 0:
            # Importar e executar criar_topicos
            import sys
            import os
            sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            
            # Criar tópicos manualmente
            topicos_data = [
                # Informática (50% - 27 tópicos)
                ("Informática", "Hardware", "Componentes internos (CPU, RAM, HD, SSD, placa-mãe)", None),
                ("Informática", "Hardware", "Periféricos de entrada e saída", None),
                ("Informática", "Redes", "Conceitos básicos de redes (LAN, WAN, MAN)", None),
                ("Informática", "Redes", "Protocolos TCP/IP", None),
                ("Informática", "Redes", "Equipamentos de rede (switch, roteador, hub)", None),
                ("Informática", "Sistemas Operacionais", "Windows 10/11", None),
                ("Informática", "Sistemas Operacionais", "Linux básico", None),
                ("Informática", "Microsoft Office", "Word (formatação, tabelas, estilos)", None),
                ("Informática", "Microsoft Office", "Excel (fórmulas, funções, gráficos)", None),
                ("Informática", "Microsoft Office", "PowerPoint (apresentações)", None),
                ("Informática", "Segurança da Informação", "Conceitos de segurança", None),
                ("Informática", "Segurança da Informação", "Backup e recuperação", None),
                ("Informática", "Internet", "Navegadores e ferramentas de busca", None),
                ("Informática", "Internet", "E-mail e comunicação", None),
                ("Informática", "Manutenção", "Manutenção preventiva e corretiva", None),
                
                # Português (15% - 8 tópicos)
                ("Português", "Interpretação de Texto", "Compreensão e interpretação", None),
                ("Português", "Gramática", "Concordância verbal e nominal", None),
                ("Português", "Gramática", "Regência verbal e nominal", None),
                ("Português", "Gramática", "Crase", None),
                ("Português", "Ortografia", "Acentuação gráfica", None),
                ("Português", "Pontuação", "Uso correto de vírgula, ponto, etc", None),
                
                # Matemática (10% - 6 tópicos)
                ("Matemática", "Aritmética", "Operações básicas", None),
                ("Matemática", "Porcentagem", "Cálculos percentuais", None),
                ("Matemática", "Regra de Três", "Simples e composta", None),
                ("Matemática", "Frações", "Operações com frações", None),
                
                # Raciocínio Lógico (7% - 4 tópicos)
                ("Raciocínio Lógico", "Sequências", "Lógicas e numéricas", None),
                ("Raciocínio Lógico", "Proposições", "Lógica proposicional", None),
                
                # Legislação (11% - 6 tópicos)
                ("Legislação", "Estatuto dos Servidores de Rondônia", "Direitos e deveres", None),
                ("Legislação", "Ética no Serviço Público", "Princípios éticos", None),
                ("Legislação", "Lei de Licitações", "Lei 14.133/2021", None),
                
                # Conhecimentos Gerais (7% - 3 tópicos)
                ("Conhecimentos Gerais", "Rondônia", "Geografia e economia", None),
                ("Conhecimentos Gerais", "Porto Velho", "História e atualidades", None),
                ("Conhecimentos Gerais", "Atualidades", "Brasil e região Norte", None),
            ]
            
            for disciplina, topico, subtopico, ref in topicos_data:
                topic = Topic(
                    disciplina=disciplina,
                    topico=topico,
                    subtopico=subtopico,
                    reference=ref
                )
                db.add(topic)
            
            db.commit()
            results["topics"] = len(topicos_data)
        else:
            results["topics"] = topics_count
        
        # Criar usuário de teste se não existir
        existing_user = db.query(User).filter(User.username == "teste").first()
        if not existing_user:
            user = User(
                username="teste",
                email="teste@portovelho.com",
                hashed_password=pwd_context.hash("teste123"),
                full_name="Usuário Teste"
            )
            db.add(user)
            db.commit()
            results["user"] = "created"
        
        return {
            "status": "success",
            "message": "Sistema inicializado com sucesso!",
            "details": results
        }
        
    except Exception as e:
        logger.error(f"Erro ao inicializar sistema: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/api/seed-simple")
async def seed_simple(db: Session = Depends(get_db)):
    """
    Endpoint simplificado para criar apenas o usuário de teste.
    """
    try:
        from models import User
        import bcrypt
        
        # Verificar se já existe
        existing = db.query(User).filter(User.username == "teste").first()
        if existing:
            return {"status": "exists", "message": "Usuário já existe"}
        
        # Criar hash manualmente com bcrypt
        senha = "teste123".encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(senha, salt).decode('utf-8')
        
        user = User(
            email="teste@example.com",
            username="teste",
            hashed_password=hashed,
            full_name="Usuário Teste"
        )
        db.add(user)
        db.commit()
        
        return {
            "status": "success",
            "message": "Usuário criado!",
            "credentials": {"username": "teste", "password": "teste123"}
        }
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}

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
        
        # Criar usuário de teste com senha curta (bcrypt tem limite de 72 bytes)
        senha_teste = "teste123"[:72]  # Garantir que não exceda 72 bytes
        hashed_pwd = get_password_hash(senha_teste)
        
        user = User(
            email="teste@example.com",
            username="teste",
            hashed_password=hashed_pwd,
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
                "password": "teste123"
            }
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao popular banco de dados: {str(e)}"
        )
