@echo off
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║     🚀 DEPLOY NO RENDER - Sistema Porto Velho                 ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo 📋 Preparando código para deploy...
echo.

REM Verificar se está no diretório correto
if not exist "api" (
    echo ❌ Erro: Execute este script na raiz do projeto!
    pause
    exit /b 1
)

echo ✅ Diretório correto
echo.

echo 📦 Adicionando arquivos ao Git...
git add .

echo.
echo 💬 Fazendo commit...
git commit -m "Deploy: Sistema Porto Velho - Pronto para Render"

echo.
echo 🚀 Enviando para GitHub...
git push origin main

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║     ✅ CÓDIGO ATUALIZADO NO GITHUB!                           ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo 🌐 Próximos passos:
echo.
echo 1. Acesse: https://dashboard.render.com
echo 2. Crie Web Service (API):
echo    - Repositório: Dev-HP/simulados-ibgp
echo    - Root Directory: api
echo    - Environment: Docker
echo.
echo 3. Adicione variáveis de ambiente:
echo    GEMINI_API_KEY=AIzaSyBYpSeQqF5k3hyAuLPZw5V-suXwLnGj7XM
echo    DATABASE_URL=sqlite:///./simulados.db
echo    SECRET_KEY=render-secret-key-2026
echo.
echo 4. Crie Static Site (Frontend):
echo    - Repositório: Dev-HP/simulados-ibgp
echo    - Root Directory: web
echo    - Build: npm install ^&^& npm run build
echo    - Publish: web/dist
echo.
echo 5. Adicione variável no Frontend:
echo    VITE_API_URL=https://sua-api.onrender.com
echo.
echo 📚 Guia completo: DEPLOY_RENDER.md
echo.

pause
