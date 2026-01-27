@echo off
echo ========================================
echo POPULANDO BANCO DE DADOS
echo ========================================
echo.
echo Aguarde...
echo.

curl https://simulados-ibgp.onrender.com/api/seed-database

echo.
echo.
echo ========================================
echo PRONTO!
echo ========================================
echo.
echo Agora voce pode acessar:
echo https://simulados-ibgp-1.onrender.com
echo.
echo Login:
echo Usuario: teste
echo Senha: senha123
echo ========================================
pause
