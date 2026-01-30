@echo off
REM Script automatizado para setup no GitHub (Windows)
REM Execute: setup_github.bat

echo ========================================
echo Setup Automatico - GitHub (Windows)
echo ========================================
echo.

REM Verificar se Git esta instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Git nao esta instalado!
    echo Instale Git: https://git-scm.com/downloads
    pause
    exit /b 1
)
echo [OK] Git instalado

echo.
echo ========================================
echo Informacoes do GitHub
echo ========================================
echo.

set /p github_user="Seu username do GitHub: "
set /p repo_name="Nome do repositorio (padrao: simulados-ibgp): "
if "%repo_name%"=="" set repo_name=simulados-ibgp

echo.
echo Repositorio sera criado em: https://github.com/%github_user%/%repo_name%
echo.
set /p confirm="Continuar? (s/n): "
if /i not "%confirm%"=="s" (
    echo Cancelado pelo usuario
    pause
    exit /b 1
)

echo.
echo ========================================
echo Configurando Git
echo ========================================
echo.

REM Verificar se ja e um repositorio Git
if exist ".git" (
    echo [INFO] Repositorio Git ja existe
) else (
    echo [INFO] Inicializando repositorio Git...
    git init
    echo [OK] Repositorio inicializado
)

echo.
echo [INFO] Adicionando arquivos...
git add .
echo [OK] Arquivos adicionados

echo.
echo [INFO] Criando commit inicial...
git commit -m "Initial commit: Sistema completo de simulados IBGP"
echo [OK] Commit criado

echo.
echo [INFO] Criando branch main...
git branch -M main
echo [OK] Branch main criada

echo.
echo [INFO] Conectando com GitHub...
git remote remove origin 2>nul
git remote add origin https://github.com/%github_user%/%repo_name%.git
echo [OK] Remote adicionado

echo.
echo ========================================
echo Fazendo Push para GitHub
echo ========================================
echo.
echo Voce precisara fazer login no GitHub...
echo.

git push -u origin main

if errorlevel 1 (
    echo.
    echo [ERRO] Erro ao fazer push!
    echo.
    echo Possiveis solucoes:
    echo 1. Verifique se o repositorio existe no GitHub
    echo    Crie em: https://github.com/new
    echo.
    echo 2. Configure autenticacao:
    echo    - Token: https://github.com/settings/tokens
    echo.
    echo 3. Tente manualmente:
    echo    git push -u origin main
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo [OK] Push concluido com sucesso!
echo ========================================
echo.
echo Seu repositorio esta no GitHub!
echo.
echo URL do Repositorio:
echo    https://github.com/%github_user%/%repo_name%
echo.
echo Proximos Passos:
echo    1. Acesse: https://github.com/%github_user%/%repo_name%
echo    2. Verifique se todos os arquivos estao la
echo    3. Configure GitHub Actions (ja esta pronto!)
echo    4. Faca deploy online (veja GITHUB_SETUP.md)
echo.
echo Guias Disponiveis:
echo    - GITHUB_SETUP.md: Deploy online completo
echo    - docs\DEPLOYMENT.md: Opcoes de deploy
echo    - docs\QUICKSTART.md: Como usar o sistema
echo.
echo Opcoes de Deploy Gratuito:
echo    - Render.com (recomendado)
echo    - Railway.app
echo    - Fly.io
echo    - Heroku
echo.
echo Veja instrucoes detalhadas em: GITHUB_SETUP.md
echo.

set /p create_tag="Criar tag de release v1.0.0? (s/n): "
if /i "%create_tag%"=="s" (
    git tag -a v1.0.0 -m "Release 1.0.0: Sistema completo de simulados IBGP"
    git push origin v1.0.0
    echo [OK] Tag v1.0.0 criada e enviada
    echo.
    echo Crie uma release no GitHub:
    echo    https://github.com/%github_user%/%repo_name%/releases/new
)

echo.
echo ========================================
echo Setup Completo!
echo ========================================
echo.
pause
