@echo off
echo ================================================================================
echo   IMPORTADOR DE PROVAS DE REFERENCIA
echo ================================================================================
echo.

echo [1/2] Verificando se a API esta rodando...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERRO: API nao esta rodando!
    echo.
    echo Execute em outro terminal:
    echo   cd api
    echo   uvicorn main:app --reload
    echo.
    pause
    exit /b 1
)

echo OK - API esta rodando
echo.

echo [2/2] Importando provas...
python importar_provas.py

echo.
pause
