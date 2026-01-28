@echo off
chcp 65001 >nul
title Sistema de Preparação - Câmara de Porto Velho

:menu
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║     🎯 SISTEMA DE PREPARAÇÃO PARA CONCURSO                    ║
echo ║     Técnico em Informática - Câmara de Porto Velho/RO         ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo  📋 MENU PRINCIPAL
echo  ═══════════════════════════════════════════════════════════════
echo.
echo  [1] 🚀 Iniciar Sistema (API + Frontend)
echo  [2] 📊 Ver Estatísticas do Banco
echo  [3] 🤖 Gerar Questões Massivas com IA
echo  [4] 📝 Criar/Atualizar Tópicos
echo  [5] 📚 Importar Provas de Referência
echo  [6] 🧪 Testar Sistema Completo
echo  [7] 📖 Abrir Guia Completo
echo  [8] ❌ Sair
echo.
echo  ═══════════════════════════════════════════════════════════════
echo.
set /p opcao="  Escolha uma opção: "

if "%opcao%"=="1" goto iniciar
if "%opcao%"=="2" goto estatisticas
if "%opcao%"=="3" goto gerar_questoes
if "%opcao%"=="4" goto criar_topicos
if "%opcao%"=="5" goto importar_provas
if "%opcao%"=="6" goto testar
if "%opcao%"=="7" goto guia
if "%opcao%"=="8" goto sair

echo.
echo  ❌ Opção inválida!
timeout /t 2 >nul
goto menu

:iniciar
cls
echo.
echo  🚀 Iniciando Sistema...
echo  ═══════════════════════════════════════════════════════════════
echo.
call iniciar_sistema.bat
goto menu

:estatisticas
cls
echo.
echo  📊 Estatísticas do Banco de Questões
echo  ═══════════════════════════════════════════════════════════════
echo.
python -c "import sys; sys.path.insert(0, 'api'); from database import SessionLocal; from models import Question, Topic; db = SessionLocal(); print(f'\n  Total de Questões: {db.query(Question).count()}'); print(f'  Total de Tópicos: {db.query(Topic).count()}\n'); disciplinas = db.query(Question.disciplina).distinct().all(); print('  Por Disciplina:'); [print(f'    • {d[0]:25s}: {db.query(Question).filter(Question.disciplina == d[0]).count():4d} questões') for d in disciplinas]; db.close()"
echo.
echo  ═══════════════════════════════════════════════════════════════
pause
goto menu

:gerar_questoes
cls
echo.
echo  🤖 Geração Massiva de Questões com IA
echo  ═══════════════════════════════════════════════════════════════
echo.
echo  ⚠️  ATENÇÃO:
echo  • Este processo pode levar 2-4 horas
echo  • Gerará 500-800 questões automaticamente
echo  • Respeita o rate limit do Gemini (gratuito)
echo  • Você pode cancelar a qualquer momento (Ctrl+C)
echo.
echo  ═══════════════════════════════════════════════════════════════
echo.
set /p confirma="  Deseja continuar? (S/N): "
if /i "%confirma%"=="S" (
    python gerar_questoes_concurso.py
) else (
    echo.
    echo  ❌ Operação cancelada
    timeout /t 2 >nul
)
goto menu

:criar_topicos
cls
echo.
echo  📝 Criar/Atualizar Tópicos
echo  ═══════════════════════════════════════════════════════════════
echo.
python criar_topicos.py
echo.
echo  ═══════════════════════════════════════════════════════════════
pause
goto menu

:importar_provas
cls
echo.
echo  📚 Importar Provas de Referência
echo  ═══════════════════════════════════════════════════════════════
echo.
echo  Coloque os PDFs das provas em: data\provas_referencia\
echo.
call importar_provas.bat
echo.
echo  ═══════════════════════════════════════════════════════════════
pause
goto menu

:testar
cls
echo.
echo  🧪 Testando Sistema Completo
echo  ═══════════════════════════════════════════════════════════════
echo.
call start_and_test.bat
goto menu

:guia
cls
echo.
echo  📖 Abrindo Guia Completo...
echo.
start GUIA_COMPLETO_CONCURSO.md
timeout /t 2 >nul
goto menu

:sair
cls
echo.
echo  ═══════════════════════════════════════════════════════════════
echo.
echo     ✅ Obrigado por usar o Sistema de Preparação!
echo.
echo     💪 Boa sorte nos estudos!
echo     🎯 Você vai conseguir!
echo.
echo  ═══════════════════════════════════════════════════════════════
echo.
timeout /t 3 >nul
exit
