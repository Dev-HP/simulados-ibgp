#!/bin/bash

# Script automatizado para setup no GitHub
# Execute: bash setup_github.sh

echo "🚀 Setup Automático - GitHub"
echo "=============================="
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para perguntar
ask() {
    echo -e "${BLUE}$1${NC}"
    read -r response
    echo "$response"
}

# Função para sucesso
success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Função para erro
error() {
    echo -e "${RED}✗${NC} $1"
}

# Função para info
info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

echo "Este script irá:"
echo "1. Inicializar repositório Git"
echo "2. Fazer commit inicial"
echo "3. Conectar com GitHub"
echo "4. Fazer push"
echo ""

# Verificar se Git está instalado
if ! command -v git &> /dev/null; then
    error "Git não está instalado!"
    echo "Instale Git: https://git-scm.com/downloads"
    exit 1
fi
success "Git instalado"

# Verificar se já é um repositório Git
if [ -d ".git" ]; then
    info "Repositório Git já existe"
    existing_repo=true
else
    existing_repo=false
fi

# Pedir informações do usuário
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Informações do GitHub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

github_user=$(ask "Seu username do GitHub:")
repo_name=$(ask "Nome do repositório (padrão: simulados-ibgp):")
repo_name=${repo_name:-simulados-ibgp}

echo ""
info "Repositório será criado em: https://github.com/$github_user/$repo_name"
echo ""

read -p "Continuar? (s/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    error "Cancelado pelo usuário"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Configurando Git"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Configurar Git (se necessário)
if [ -z "$(git config user.name)" ]; then
    git_name=$(ask "Seu nome para commits:")
    git config user.name "$git_name"
    success "Nome configurado: $git_name"
fi

if [ -z "$(git config user.email)" ]; then
    git_email=$(ask "Seu email para commits:")
    git config user.email "$git_email"
    success "Email configurado: $git_email"
fi

# Inicializar repositório
if [ "$existing_repo" = false ]; then
    echo ""
    info "Inicializando repositório Git..."
    git init
    success "Repositório inicializado"
fi

# Adicionar arquivos
echo ""
info "Adicionando arquivos..."
git add .
success "Arquivos adicionados"

# Commit
echo ""
info "Criando commit inicial..."
git commit -m "Initial commit: Sistema completo de simulados IBGP

- Backend FastAPI completo
- Frontend React + Vite
- Docker + Docker Compose
- PostgreSQL + Redis
- CI/CD GitHub Actions
- Documentação completa
- Testes automatizados
- Dados de amostra

Sistema pronto para produção!"

success "Commit criado"

# Criar branch main
echo ""
info "Criando branch main..."
git branch -M main
success "Branch main criada"

# Adicionar remote
echo ""
info "Conectando com GitHub..."
remote_url="https://github.com/$github_user/$repo_name.git"

# Remover remote existente se houver
git remote remove origin 2>/dev/null

git remote add origin "$remote_url"
success "Remote adicionado: $remote_url"

# Push
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Fazendo Push para GitHub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

info "Você precisará fazer login no GitHub..."
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    success "Push concluído com sucesso!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🎉 Seu repositório está no GitHub!"
    echo ""
    echo "📍 URL do Repositório:"
    echo "   https://github.com/$github_user/$repo_name"
    echo ""
    echo "📍 Próximos Passos:"
    echo "   1. Acesse: https://github.com/$github_user/$repo_name"
    echo "   2. Verifique se todos os arquivos estão lá"
    echo "   3. Configure GitHub Actions (já está pronto!)"
    echo "   4. Faça deploy online (veja GITHUB_SETUP.md)"
    echo ""
    echo "📚 Guias Disponíveis:"
    echo "   - GITHUB_SETUP.md: Deploy online completo"
    echo "   - docs/DEPLOYMENT.md: Opções de deploy"
    echo "   - docs/QUICKSTART.md: Como usar o sistema"
    echo ""
    echo "🚀 Opções de Deploy Gratuito:"
    echo "   - Render.com (recomendado)"
    echo "   - Railway.app"
    echo "   - Fly.io"
    echo "   - Heroku"
    echo ""
    echo "Veja instruções detalhadas em: GITHUB_SETUP.md"
    echo ""
else
    echo ""
    error "Erro ao fazer push!"
    echo ""
    echo "Possíveis soluções:"
    echo "1. Verifique se o repositório existe no GitHub"
    echo "   Crie em: https://github.com/new"
    echo ""
    echo "2. Configure autenticação:"
    echo "   - Token: https://github.com/settings/tokens"
    echo "   - SSH: https://docs.github.com/en/authentication"
    echo ""
    echo "3. Tente manualmente:"
    echo "   git push -u origin main"
    echo ""
    exit 1
fi

# Criar tag de release
echo ""
read -p "Criar tag de release v1.0.0? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    git tag -a v1.0.0 -m "Release 1.0.0: Sistema completo de simulados IBGP"
    git push origin v1.0.0
    success "Tag v1.0.0 criada e enviada"
    echo ""
    info "Crie uma release no GitHub:"
    echo "   https://github.com/$github_user/$repo_name/releases/new"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup Completo!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
