@echo off
echo ========================================
echo   TESTE LOCAL - Sistema de Simulados
echo ========================================
echo.

echo [1/5] Verificando dependencias...
python --version
node --version
echo.

echo [2/5] Instalando dependencias da API...
cd api
pip install -r requirements.txt
cd ..
echo.

echo [3/5] Instalando dependencias do Frontend...
cd web
call npm install
cd ..
echo.

echo [4/5] Iniciando banco de dados (Docker)...
docker-compose up -d postgres
timeout /t 5
echo.

echo [5/5] Sistema pronto para teste!
echo.
echo ========================================
echo   PROXIMOS PASSOS:
echo ========================================
echo.
echo 1. Terminal 1 - Iniciar API:
echo    cd api
echo    uvicorn main:app --reload --host 0.0.0.0 --port 8000
echo.
echo 2. Terminal 2 - Iniciar Frontend:
echo    cd web
echo    npm run dev
echo.
echo 3. Acessar:
echo    Frontend: http://localhost:3000
echo    API Docs: http://localhost:8000/docs
echo.
echo 4. Testar Gemini AI:
echo    - Faca login (teste/teste123)
echo    - Va em "IA Questoes"
echo    - Importe uma prova real
echo    - Gere questoes com IA
echo.
echo ========================================

pause
