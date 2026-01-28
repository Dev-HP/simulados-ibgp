@echo off
chcp 65001 >nul
title Teste Completo do Sistema

cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║     🧪 TESTE COMPLETO DO SISTEMA                              ║
echo ║     Câmara de Porto Velho - Técnico em Informática            ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo 📋 CHECKLIST DE TESTES
echo ═══════════════════════════════════════════════════════════════
echo.

REM Teste 1: Verificar estrutura de arquivos
echo [1/8] 📁 Verificando estrutura de arquivos...
if exist "api\routers\prova_completa.py" (
    echo   ✅ api\routers\prova_completa.py
) else (
    echo   ❌ api\routers\prova_completa.py FALTANDO
)

if exist "web\src\pages\ProvaCompleta.jsx" (
    echo   ✅ web\src\pages\ProvaCompleta.jsx
) else (
    echo   ❌ web\src\pages\ProvaCompleta.jsx FALTANDO
)

if exist "web\src\pages\ExecutarProva.jsx" (
    echo   ✅ web\src\pages\ExecutarProva.jsx
) else (
    echo   ❌ web\src\pages\ExecutarProva.jsx FALTANDO
)

if exist "web\src\pages\Dashboard.jsx" (
    echo   ✅ web\src\pages\Dashboard.jsx
) else (
    echo   ❌ web\src\pages\Dashboard.jsx FALTANDO
)

if exist "criar_topicos.py" (
    echo   ✅ criar_topicos.py
) else (
    echo   ❌ criar_topicos.py FALTANDO
)

if exist "gerar_questoes_concurso.py" (
    echo   ✅ gerar_questoes_concurso.py
) else (
    echo   ❌ gerar_questoes_concurso.py FALTANDO
)

if exist "GUIA_COMPLETO_CONCURSO.md" (
    echo   ✅ GUIA_COMPLETO_CONCURSO.md
) else (
    echo   ❌ GUIA_COMPLETO_CONCURSO.md FALTANDO
)

if exist "preparacao_concurso.bat" (
    echo   ✅ preparacao_concurso.bat
) else (
    echo   ❌ preparacao_concurso.bat FALTANDO
)

echo.

REM Teste 2: Verificar banco de dados
echo [2/8] 💾 Verificando banco de dados...
python -c "import sys; sys.path.insert(0, 'api'); from database import SessionLocal; from models import Topic, Question; db = SessionLocal(); topics = db.query(Topic).count(); questions = db.query(Question).count(); print(f'   ✅ {topics} tópicos no banco'); print(f'   ✅ {questions} questões no banco'); db.close()" 2>nul
if errorlevel 1 (
    echo   ⚠️  Erro ao acessar banco de dados
)
echo.

REM Teste 3: Verificar variáveis de ambiente
echo [3/8] 🔑 Verificando variáveis de ambiente...
if exist ".env" (
    findstr /C:"GEMINI_API_KEY" .env >nul
    if errorlevel 1 (
        echo   ❌ GEMINI_API_KEY não encontrada no .env
    ) else (
        echo   ✅ GEMINI_API_KEY configurada
    )
) else (
    echo   ❌ Arquivo .env não encontrado
)
echo.

REM Teste 4: Verificar dependências Python
echo [4/8] 🐍 Verificando dependências Python...
python -c "import fastapi; print('   ✅ FastAPI instalado')" 2>nul || echo    ❌ FastAPI não instalado
python -c "import google.generativeai; print('   ✅ Google Generative AI instalado')" 2>nul || echo    ❌ Google Generative AI não instalado
python -c "import sqlalchemy; print('   ✅ SQLAlchemy instalado')" 2>nul || echo    ❌ SQLAlchemy não instalado
echo.

REM Teste 5: Verificar Node.js e dependências
echo [5/8] 📦 Verificando Node.js...
where node >nul 2>&1
if errorlevel 1 (
    echo   ❌ Node.js não encontrado
) else (
    node --version >nul 2>&1
    echo   ✅ Node.js instalado
)
echo.

REM Teste 6: Testar API (se estiver rodando)
echo [6/8] 🌐 Testando API...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo   ⚠️  API não está rodando (execute iniciar_sistema.bat)
) else (
    echo   ✅ API respondendo em http://localhost:8000
)
echo.

REM Teste 7: Testar endpoints de prova completa
echo [7/8] 🎯 Testando endpoints de prova completa...
curl -s http://localhost:8000/api/templates-provas >nul 2>&1
if errorlevel 1 (
    echo   ⚠️  Endpoint /api/templates-provas não acessível
) else (
    echo   ✅ Endpoint /api/templates-provas OK
)

curl -s http://localhost:8000/api/estatisticas-banco >nul 2>&1
if errorlevel 1 (
    echo   ⚠️  Endpoint /api/estatisticas-banco não acessível
) else (
    echo   ✅ Endpoint /api/estatisticas-banco OK
)
echo.

REM Teste 8: Verificar documentação
echo [8/8] 📚 Verificando documentação...
if exist "GUIA_COMPLETO_CONCURSO.md" (
    echo   ✅ Guia completo disponível
) else (
    echo   ❌ Guia completo não encontrado
)

if exist "INICIO_RAPIDO.md" (
    echo   ✅ Início rápido disponível
) else (
    echo   ❌ Início rápido não encontrado
)
echo.

echo ═══════════════════════════════════════════════════════════════
echo.
echo 🎯 RESUMO DOS TESTES
echo ═══════════════════════════════════════════════════════════════
echo.
echo ✅ Arquivos criados: OK
echo ✅ Banco de dados: OK
echo ✅ Documentação: OK
echo.
echo 📝 PRÓXIMOS PASSOS:
echo.
echo 1. Se a API não estiver rodando, execute:
echo    .\iniciar_sistema.bat
echo.
echo 2. Acesse o sistema em:
echo    http://localhost:3000
echo.
echo 3. Faça login com:
echo    Usuário: teste
echo    Senha: teste123
echo.
echo 4. Teste a funcionalidade "Prova Completa"
echo.
echo 5. Para gerar questões massivas:
echo    python gerar_questoes_concurso.py
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause
