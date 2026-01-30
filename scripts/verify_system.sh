#!/bin/bash

# Script de verificação do sistema
# Verifica se todos os componentes estão funcionando corretamente

echo "🔍 Verificando Sistema de Simulados IBGP..."
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para verificar
check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1"
        return 1
    fi
}

# 1. Verificar Docker
echo "1. Verificando Docker..."
docker --version > /dev/null 2>&1
check "Docker instalado"

docker-compose --version > /dev/null 2>&1
check "Docker Compose instalado"

# 2. Verificar containers
echo ""
echo "2. Verificando containers..."
docker-compose ps | grep -q "Up"
check "Containers rodando"

# 3. Verificar PostgreSQL
echo ""
echo "3. Verificando PostgreSQL..."
docker-compose exec -T postgres pg_isready > /dev/null 2>&1
check "PostgreSQL respondendo"

# 4. Verificar Redis
echo ""
echo "4. Verificando Redis..."
docker-compose exec -T redis redis-cli ping > /dev/null 2>&1
check "Redis respondendo"

# 5. Verificar API
echo ""
echo "5. Verificando API..."
curl -s http://localhost:8000/health > /dev/null 2>&1
check "API respondendo"

curl -s http://localhost:8000/docs > /dev/null 2>&1
check "Swagger disponível"

# 6. Verificar Web
echo ""
echo "6. Verificando Frontend..."
curl -s http://localhost:3000 > /dev/null 2>&1
check "Frontend respondendo"

# 7. Verificar estrutura de arquivos
echo ""
echo "7. Verificando estrutura de arquivos..."
[ -f "docker-compose.yml" ]
check "docker-compose.yml existe"

[ -f ".env.example" ]
check ".env.example existe"

[ -f "README.md" ]
check "README.md existe"

[ -d "api" ]
check "Diretório api/ existe"

[ -d "web" ]
check "Diretório web/ existe"

[ -d "data" ]
check "Diretório data/ existe"

[ -f "data/pasted_content.txt" ]
check "Edital de exemplo existe"

# 8. Verificar banco de dados
echo ""
echo "8. Verificando banco de dados..."
docker-compose exec -T postgres psql -U simulados_user -d simulados_db -c "SELECT COUNT(*) FROM users;" > /dev/null 2>&1
check "Tabela users existe"

docker-compose exec -T postgres psql -U simulados_user -d simulados_db -c "SELECT COUNT(*) FROM questions;" > /dev/null 2>&1
check "Tabela questions existe"

# 9. Verificar endpoints da API
echo ""
echo "9. Verificando endpoints da API..."
curl -s http://localhost:8000/api/topics > /dev/null 2>&1
check "Endpoint /api/topics"

curl -s http://localhost:8000/api/questions > /dev/null 2>&1
check "Endpoint /api/questions"

curl -s http://localhost:8000/api/simulados > /dev/null 2>&1
check "Endpoint /api/simulados"

# 10. Verificar logs
echo ""
echo "10. Verificando logs..."
docker-compose logs api | grep -q "Application startup complete"
check "API iniciada corretamente"

docker-compose logs web | grep -q "ready in"
check "Frontend iniciado corretamente"

# Resumo
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Resumo da Verificação"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "URLs de Acesso:"
echo "  Frontend: http://localhost:3000"
echo "  API: http://localhost:8000"
echo "  Swagger: http://localhost:8000/docs"
echo ""
echo "Credenciais de Teste:"
echo "  Username: teste"
echo "  Password: senha123"
echo ""
echo "Próximos Passos:"
echo "  1. Acesse http://localhost:3000"
echo "  2. Faça upload do edital (data/pasted_content.txt)"
echo "  3. Gere banco de questões"
echo "  4. Crie e execute simulados"
echo ""
echo "Comandos Úteis:"
echo "  docker-compose logs -f        # Ver logs"
echo "  docker-compose down           # Parar containers"
echo "  docker-compose up --build     # Rebuild"
echo ""
echo -e "${GREEN}✅ Verificação concluída!${NC}"
