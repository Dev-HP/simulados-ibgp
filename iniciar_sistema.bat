@echo off
color 0A
echo.
echo ========================================
echo   SISTEMA DE SIMULADOS IBGP
echo   Inicializacao Completa
echo ========================================
echo.

echo [1/3] Verificando status dos servicos...
echo.
echo Frontend:
curl -s -o nul -w "  Status: %%{http_code}\n" https://simulados-ibgp-1.onrender.com
echo.
echo Backend:
curl -s -o nul -w "  Status: %%{http_code}\n" https://simulados-ibgp.onrender.com/health
echo.

echo [2/3] Populando banco de dados...
echo.
curl -s https://simulados-ibgp.onrender.com/api/seed-database
echo.
echo.

echo [3/3] Verificacao final...
echo.
curl -s https://simulados-ibgp.onrender.com/health
echo.
echo.

echo ========================================
echo   SISTEMA PRONTO!
echo ========================================
echo.
echo Acesse: https://simulados-ibgp-1.onrender.com
echo.
echo Credenciais de teste:
echo   Usuario: teste
echo   Senha: teste123
echo.
echo Documentacao da API:
echo   https://simulados-ibgp.onrender.com/docs
echo.
echo ========================================
pause
