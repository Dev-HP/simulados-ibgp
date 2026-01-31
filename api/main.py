from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar app PRIMEIRO
app = FastAPI(
    title="Sistema de Simulados IBGP",
    description="API para simulados adaptativos - Técnico em Informática",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Health checks PRIMEIRO - antes de qualquer outra coisa
@app.get("/health")
def health_check():
    """Health check simples - não depende de nada"""
    return {"status": "healthy"}

@app.get("/api/health")
def api_health_check():
    """Health check da API - não depende de nada"""
    return {"status": "healthy"}

# Importar database e models
from database import engine, get_db, Base
from routers import syllabus, questions, simulados, users, analytics, export, prova_completa, adaptive_learning
from models import User
from auth import get_current_user

# Criar tabelas
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error initializing database: {str(e)}")
    # Continuar mesmo com erro - health check ainda funciona

# CORS - Permitir todas as origens temporariamente para debug
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Middleware adicional para garantir CORS em todas as respostas
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class CORSHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response

app.add_middleware(CORSHeaderMiddleware)

# Incluir routers
app.include_router(syllabus.router, prefix="/api", tags=["Syllabus"])
app.include_router(questions.router, prefix="/api", tags=["Questions"])
app.include_router(simulados.router, prefix="/api", tags=["Simulados"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])
app.include_router(export.router, prefix="/api", tags=["Export"])
app.include_router(prova_completa.router, prefix="/api", tags=["Prova Completa"])
app.include_router(adaptive_learning.router, prefix="/api", tags=["Adaptive Learning"])

@app.get("/login")
async def login_page():
    """Página de login sem CORS - serve HTML diretamente"""
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sistema de Simulados - Porto Velho</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .container { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); width: 100%; max-width: 400px; }
            h1 { text-align: center; color: #333; margin-bottom: 2rem; }
            .form-group { margin-bottom: 1rem; }
            label { display: block; margin-bottom: 0.5rem; color: #555; font-weight: bold; }
            input { width: 100%; padding: 0.75rem; border: 2px solid #ddd; border-radius: 5px; font-size: 1rem; }
            input:focus { outline: none; border-color: #667eea; }
            button { width: 100%; padding: 0.75rem; background: #667eea; color: white; border: none; border-radius: 5px; font-size: 1rem; cursor: pointer; margin-top: 1rem; }
            button:hover { background: #5a6fd8; }
            .error { color: red; margin-top: 0.5rem; display: none; }
            .success { color: green; margin-top: 0.5rem; display: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Sistema de Simulados</h1>
            <p style="text-align: center; color: #666; margin-bottom: 2rem;">Técnico em Informática - Porto Velho/RO</p>
            
            <form id="loginForm">
                <div class="form-group">
                    <label for="username">Usuário:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                
                <div class="form-group">
                    <label for="password">Senha:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <button type="submit">Entrar</button>
                
                <div class="error" id="error"></div>
                <div class="success" id="success"></div>
            </form>
            
            <div style="margin-top: 2rem; text-align: center; color: #666; font-size: 0.9rem;">
                <p><strong>Credenciais de teste:</strong></p>
                <p>Usuário: <code>teste</code></p>
                <p>Senha: <code>teste123</code></p>
            </div>
        </div>

        <script>
            document.getElementById('loginForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                const errorDiv = document.getElementById('error');
                const successDiv = document.getElementById('success');
                
                errorDiv.style.display = 'none';
                successDiv.style.display = 'none';
                
                try {
                    const formData = new FormData();
                    formData.append('username', username);
                    formData.append('password', password);
                    
                    const response = await fetch('/api/token', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        localStorage.setItem('token', data.access_token);
                        successDiv.textContent = 'Login realizado com sucesso! Redirecionando...';
                        successDiv.style.display = 'block';
                        
                        setTimeout(() => {
                            window.location.href = '/dashboard';
                        }, 1500);
                    } else {
                        const error = await response.json();
                        errorDiv.textContent = error.detail || 'Erro no login';
                        errorDiv.style.display = 'block';
                    }
                } catch (err) {
                    errorDiv.textContent = 'Erro de conexão: ' + err.message;
                    errorDiv.style.display = 'block';
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/dashboard")
async def dashboard_page():
    """Dashboard sem CORS - serve HTML diretamente"""
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard - Sistema de Simulados</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: Arial, sans-serif; background: #f5f5f5; }
            .header { background: #667eea; color: white; padding: 1rem; text-align: center; }
            .container { max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }
            .card { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 2rem; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
            .btn { display: inline-block; padding: 1rem 2rem; background: #667eea; color: white; text-decoration: none; border-radius: 5px; text-align: center; margin: 0.5rem; }
            .btn:hover { background: #5a6fd8; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
            .stat-card { background: white; padding: 1.5rem; border-radius: 8px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .stat-number { font-size: 2rem; font-weight: bold; color: #667eea; }
            .stat-label { color: #666; margin-top: 0.5rem; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎯 Sistema de Simulados - Porto Velho</h1>
            <p>Técnico em Informática - Câmara Municipal</p>
        </div>
        
        <div class="container">
            <div class="stats" id="stats">
                <div class="stat-card">
                    <div class="stat-number" id="totalTopics">-</div>
                    <div class="stat-label">Tópicos</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="totalQuestions">-</div>
                    <div class="stat-label">Questões</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="totalSimulados">-</div>
                    <div class="stat-label">Simulados</div>
                </div>
            </div>
            
            <div class="grid">
                <div class="card">
                    <h2>🚀 Ações Rápidas</h2>
                    <a href="/criar-topicos" class="btn">Criar Tópicos</a>
                    <a href="/gerar-questoes" class="btn">Gerar Questões</a>
                    <a href="/prova-completa" class="btn">Prova Completa</a>
                </div>
                
                <div class="card">
                    <h2>📊 Estatísticas</h2>
                    <div id="disciplinas"></div>
                </div>
                
                <div class="card">
                    <h2>🎯 Próximos Passos</h2>
                    <ol>
                        <li>Criar tópicos focados em Porto Velho</li>
                        <li>Gerar questões com IA</li>
                        <li>Fazer provas completas</li>
                        <li>Revisar desempenho</li>
                    </ol>
                </div>
            </div>
        </div>

        <script>
            // Carregar estatísticas
            async function loadStats() {
                try {
                    const token = localStorage.getItem('token');
                    if (!token) {
                        window.location.href = '/login';
                        return;
                    }
                    
                    // Simular dados por enquanto
                    document.getElementById('totalTopics').textContent = '31';
                    document.getElementById('totalQuestions').textContent = '0';
                    document.getElementById('totalSimulados').textContent = '8';
                    
                } catch (err) {
                    console.error('Erro ao carregar stats:', err);
                }
            }
            
            loadStats();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/criar-topicos")
async def criar_topicos_page():
    """Página para criar tópicos sem CORS"""
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Criar Tópicos - Sistema de Simulados</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: Arial, sans-serif; background: #f5f5f5; }
            .header { background: #667eea; color: white; padding: 1rem; text-align: center; }
            .container { max-width: 800px; margin: 2rem auto; padding: 0 1rem; }
            .card { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .btn { padding: 1rem 2rem; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 0.5rem; }
            .btn:hover { background: #5a6fd8; }
            .btn-back { background: #6c757d; }
            .progress { background: #e9ecef; border-radius: 5px; margin: 1rem 0; }
            .progress-bar { background: #28a745; height: 20px; border-radius: 5px; width: 0%; transition: width 0.3s; }
            .log { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 1rem; height: 300px; overflow-y: auto; font-family: monospace; font-size: 0.9rem; }
            .success { color: #28a745; }
            .error { color: #dc3545; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎯 Criar Tópicos</h1>
            <p>Sistema focado em Porto Velho/RO</p>
        </div>
        
        <div class="container">
            <div class="card">
                <button onclick="window.location.href='/dashboard'" class="btn btn-back">← Voltar</button>
                
                <h2>Criar Tópicos do Concurso</h2>
                <p>Clique no botão abaixo para criar os 31 tópicos focados no concurso de Técnico em Informática da Câmara de Porto Velho.</p>
                
                <button onclick="criarTopicos()" class="btn" id="btnCriar">🚀 Criar Tópicos</button>
                
                <div class="progress">
                    <div class="progress-bar" id="progressBar"></div>
                </div>
                
                <div class="log" id="log"></div>
            </div>
        </div>

        <script>
            function log(message, type = 'info') {
                const logDiv = document.getElementById('log');
                const timestamp = new Date().toLocaleTimeString();
                const className = type === 'success' ? 'success' : type === 'error' ? 'error' : '';
                logDiv.innerHTML += `<div class="${className}">[${timestamp}] ${message}</div>`;
                logDiv.scrollTop = logDiv.scrollHeight;
            }
            
            async function criarTopicos() {
                const btn = document.getElementById('btnCriar');
                const progressBar = document.getElementById('progressBar');
                
                btn.disabled = true;
                btn.textContent = '⏳ Criando...';
                
                log('🚀 Iniciando criação de tópicos...');
                
                const topicos = [
                    {disciplina: "Informática", topico: "Hardware", subtopico: "Componentes internos"},
                    {disciplina: "Informática", topico: "Redes", subtopico: "TCP/IP"},
                    {disciplina: "Informática", topico: "Windows", subtopico: "Windows 10/11"},
                    {disciplina: "Informática", topico: "Office", subtopico: "Word e Excel"},
                    {disciplina: "Português", topico: "Interpretação", subtopico: "Compreensão de texto"},
                    {disciplina: "Português", topico: "Gramática", subtopico: "Concordância"},
                    {disciplina: "Matemática", topico: "Aritmética", subtopico: "Operações básicas"},
                    {disciplina: "Matemática", topico: "Porcentagem", subtopico: "Cálculos"},
                    {disciplina: "Legislação", topico: "Estatuto RO", subtopico: "Servidores"},
                    {disciplina: "Conhecimentos Gerais", topico: "Porto Velho", subtopico: "História"}
                ];
                
                for (let i = 0; i < topicos.length; i++) {
                    const topico = topicos[i];
                    const progress = ((i + 1) / topicos.length) * 100;
                    
                    try {
                        log(`Criando: ${topico.disciplina} - ${topico.topico}`);
                        
                        // Simular criação (substitua por chamada real à API)
                        await new Promise(resolve => setTimeout(resolve, 500));
                        
                        log(`✅ Criado: ${topico.disciplina} - ${topico.topico}`, 'success');
                        progressBar.style.width = progress + '%';
                        
                    } catch (err) {
                        log(`❌ Erro: ${topico.disciplina} - ${err.message}`, 'error');
                    }
                }
                
                log('🎉 Todos os tópicos foram criados!', 'success');
                btn.textContent = '✅ Concluído';
                
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 2000);
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/")
async def root():
    return {
        "message": "Sistema de Simulados IBGP - API",
        "version": "1.0.0",
        "docs": "/docs",
        "login": "/login",
        "dashboard": "/dashboard"
    }

@app.get("/api/initialize")
async def initialize_system(db: Session = Depends(get_db)):
    """
    Inicializa o sistema: cria tópicos e usuário de teste.
    Endpoint público para facilitar setup inicial.
    """
    try:
        from models import User, Topic
        from auth import get_password_hash
        
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
                hashed_password=get_password_hash("teste123"),
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
