@echo off
echo ========================================
echo TESTANDO DEPLOY DO SISTEMA SIMULADOS
echo ========================================
echo.

echo [1/4] Testando Frontend...
curl -s -o nul -w "Status: %%{http_code}\n" https://simulados-ibgp-1.onrender.com
echo.

echo [2/4] Testando Backend - Health Check...
curl -s -o nul -w "Status: %%{http_code}\n" https://simulados-ibgp.onrender.com/
echo.

echo [3/4] Testando Backend - Docs API...
curl -s -o nul -w "Status: %%{http_code}\n" https://simulados-ibgp.onrender.com/docs
echo.

echo [4/4] Testando Backend - Health Endpoint...
curl -s https://simulados-ibgp.onrender.com/health
echo.
echo.

echo ========================================
echo RESULTADO:
echo ========================================
echo - Status 200 = OK (funcionando)
echo - Status 404 = Endpoint nao encontrado
echo - Status 502/503 = Servico offline
echo - Erro de conexao = Servico nao disponivel
echo ========================================
pause
