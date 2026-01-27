@echo off
echo ========================================
echo   TESTE DO SISTEMA DE IA
echo ========================================
echo.

echo [1/5] Testando API Backend...
curl -s https://simulados-ibgp.onrender.com/api/health
echo.
echo.

echo [2/5] Testando autenticacao...
curl -s -X POST https://simulados-ibgp.onrender.com/api/token ^
  -H "Content-Type: application/x-www-form-urlencoded" ^
  -d "username=teste&password=teste123"
echo.
echo.

echo [3/5] Listando topicos disponiveis...
curl -s https://simulados-ibgp.onrender.com/api/topics
echo.
echo.

echo [4/5] Listando questoes existentes...
curl -s https://simulados-ibgp.onrender.com/api/questions?limit=5
echo.
echo.

echo [5/5] Verificando configuracao Gemini...
echo Verifique se GEMINI_API_KEY esta configurada no Render
echo Acesse: https://dashboard.render.com
echo.

echo ========================================
echo   TESTE CONCLUIDO
echo ========================================
echo.
echo Proximos passos:
echo 1. Adicione GEMINI_API_KEY no Render
echo 2. Importe questoes reais via interface web
echo 3. Gere questoes com IA
echo.
pause
