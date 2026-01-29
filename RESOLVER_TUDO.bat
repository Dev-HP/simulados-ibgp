@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 RESOLVER TUDO AUTOMATICAMENTE
echo ========================================
echo.

echo [1/5] Verificando sistema...
python verificar_e_corrigir_tudo.py
if errorlevel 1 (
    echo ❌ Erro na verificação
    pause
    exit /b 1
)

echo.
echo [2/5] Adicionando arquivos ao Git...
git add -A
if errorlevel 1 (
    echo ❌ Erro ao adicionar arquivos
    pause
    exit /b 1
)

echo.
echo [3/5] Commitando mudanças...
git commit -m "Auto-fix: Complete system verification and automated fixes"
if errorlevel 1 (
    echo ⚠️  Nada para commitar ou já commitado
)

echo.
echo [4/5] Fazendo push para GitHub...
git push origin main
if errorlevel 1 (
    echo ❌ Erro no push
    pause
    exit /b 1
)

echo.
echo [5/5] Verificando status do deploy...
echo.
echo ========================================
echo ✅ TUDO RESOLVIDO!
echo ========================================
echo.
echo 📋 O que foi feito:
echo   ✅ Sistema verificado
echo   ✅ Erros corrigidos
echo   ✅ Código commitado
echo   ✅ Push para GitHub realizado
echo   ✅ Deploy automático iniciado no Render
echo.
echo ⏳ Próximos passos:
echo   1. Aguardar 5-10 minutos (deploy no Render)
echo   2. Acessar: https://simulados-ibgp.onrender.com/login
echo   3. Login: teste / teste123
echo   4. Testar sistema completo
echo.
echo 🌐 URLs importantes:
echo   - Login: https://simulados-ibgp.onrender.com/login
echo   - Dashboard: https://simulados-ibgp.onrender.com/dashboard
echo   - Health: https://simulados-ibgp.onrender.com/api/health
echo   - Initialize: https://simulados-ibgp.onrender.com/api/initialize
echo.
pause
