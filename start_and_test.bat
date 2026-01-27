@echo off
echo ================================================================================
echo   INICIAR SISTEMA E EXECUTAR TESTES AUTOMATIZADOS
echo ================================================================================
echo.

echo [1/4] Verificando dependencias...
python --version
if errorlevel 1 (
    echo ERRO: Python nao encontrado
    pause
    exit /b 1
)

pip show requests >nul 2>&1
if errorlevel 1 (
    echo Instalando biblioteca requests...
    pip install requests
)

echo.
echo [2/4] Iniciando banco de dados...
docker-compose up -d postgres 2>nul
if errorlevel 1 (
    echo AVISO: Docker nao disponivel, usando banco local
)
timeout /t 3 >nul

echo.
echo [3/4] Iniciando API em segundo plano...
cd api
start /B cmd /c "uvicorn main:app --reload --host 0.0.0.0 --port 8000 > api.log 2>&1"
cd ..

echo Aguardando API iniciar (10 segundos)...
timeout /t 10 >nul

echo.
echo [4/4] Executando testes automatizados...
echo.
python run_all_tests.py

echo.
echo ================================================================================
echo   TESTES CONCLUIDOS
echo ================================================================================
echo.
echo Para parar a API, execute: taskkill /F /IM python.exe
echo.
pause
