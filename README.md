# Sistema de Simulados Adaptativos - Técnico em Informática (IBGP)

[![CI/CD](https://github.com/seu-usuario/simulados-ibgp/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/seu-usuario/simulados-ibgp/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sistema completo de treino adaptativo para concursos públicos com ingestão automática de editais, geração de questões no estilo IBGP, simulados configuráveis e feedback detalhado.

## ✨ Destaques

- 🎯 **Ingestão Automática**: Upload de editais TXT/PDF com parse hierárquico
- 🤖 **Geração Inteligente**: 30+ questões por tópico no estilo IBGP
- ✅ **Validação QA**: Sistema automático de qualidade de questões
- 📊 **Simulados Configuráveis**: Oficiais e customizados
- 🧠 **Treino Adaptativo**: Algoritmo SRS para otimizar aprendizado
- 📈 **Analytics Completo**: Métricas detalhadas e plano de estudo
- 🔄 **Export Fácil**: GIFT, CSV, JSON
- 🐳 **Docker Ready**: Deploy em 3 comandos

## 🚀 Quickstart Local (3 minutos)

```bash
# 1. Clone e configure
git clone <repo-url>
cd simulados-ibgp
cp .env.example .env

# 2. Inicie os containers
docker-compose up --build

# 3. Popule com dados de teste (opcional)
docker-compose exec api python scripts/seed_database.py
```

**Pronto!** Acesse:
- 🌐 Frontend: http://localhost:3000
- 🔌 API: http://localhost:8000
- 📚 Swagger: http://localhost:8000/docs

**Credenciais de teste**: `teste` / `senha123`

## 🌐 Hospedar no GitHub e Deploy Online

### Opção 1: Script Automático (Recomendado)

**Windows:**
```bash
setup_github.bat
```

**Linux/Mac:**
```bash
bash setup_github.sh
```

### Opção 2: Manual

```bash
# 1. Criar repositório no GitHub (https://github.com/new)

# 2. Inicializar e fazer push
git init
git add .
git commit -m "Initial commit: Sistema completo de simulados IBGP"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/simulados-ibgp.git
git push -u origin main
```

### Deploy Online Gratuito

Escolha uma plataforma:

1. **Render.com** (Recomendado - Mais fácil)
   - Acesse: https://render.com
   - Conecte seu repositório GitHub
   - Deploy automático com Docker
   - PostgreSQL incluído gratuitamente

2. **Railway.app** (Muito simples)
   - Acesse: https://railway.app
   - Deploy em 1 clique
   - Detecta docker-compose automaticamente

3. **Fly.io** (Rápido e global)
   - Instale CLI: `curl -L https://fly.io/install.sh | sh`
   - Deploy: `fly launch`

4. **Heroku** (Clássico)
   - Instale CLI e faça deploy
   - Addons gratuitos disponíveis

**📖 Guia Completo**: Veja [GITHUB_SETUP.md](GITHUB_SETUP.md) para instruções detalhadas de cada plataforma.

## 📋 Workflow Completo

1. **Upload Edital** → Resposta: "Conteúdo programático recebido" ✓
2. **Gerar Banco** → 30+ questões por tópico
3. **Criar Simulado** → Configurável (questões, tempo, disciplinas)
4. **Executar** → Feedback imediato + explicações
5. **Analytics** → Métricas + plano de estudo personalizado

## 📋 Funcionalidades

- ✅ Ingestão automática de editais (TXT/PDF)
- ✅ Parse hierárquico: disciplina > tópico > subtópico
- ✅ Geração automática de questões no estilo IBGP
- ✅ Validação automática (QA) de questões
- ✅ Simulados configuráveis (oficiais e customizados)
- ✅ Treino adaptativo com algoritmo SRS
- ✅ Feedback imediato e detalhado
- ✅ Métricas e analytics completos
- ✅ Export em múltiplos formatos (GIFT, CSV, JSON)
- ✅ API REST completa (OpenAPI/Swagger)

## 🏗️ Arquitetura

```
simulados-ibgp/
├── api/              # Backend FastAPI
├── web/              # Frontend React + Vite
├── infra/            # Nginx, configs
├── data/             # Editais, seeds
├── tests/            # Testes automatizados
└── docker/           # Dockerfiles
```

## 🛠️ Stack Tecnológica

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15 + Redis
- **Frontend**: React 18 + Vite + TypeScript
- **Auth**: JWT + OAuth2 (Google)
- **CI/CD**: GitHub Actions
- **Containerização**: Docker + Docker Compose

## 📚 Documentação

- [API Documentation](http://localhost:8000/docs) - Swagger/OpenAPI
- [Guia de Contribuição](CONTRIBUTING.md)
- [Templates de Issues](.github/ISSUE_TEMPLATE/)

## 🧪 Desenvolvimento Local

```bash
# Instalar dependências
make install

# Rodar em modo dev
make dev

# Executar testes
make test

# Lint e formatação
make lint
```

## 📊 Conteúdo Programático Coberto

- Hardware e componentes
- Algoritmos e estruturas de dados
- Banco de dados (SQL, modelagem ER)
- Sistemas operacionais (Linux, Windows)
- Redes (TCP/IP, protocolos)
- Segurança da informação
- Noções de Informática (Excel, atalhos)
- Legislação (LGPD, Marco Civil)

## 🤝 Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para guidelines de contribuição.

## 📄 Licença

MIT License


## 🎓 Conteúdo Programático Coberto

- ✅ Hardware (componentes, memórias, periféricos)
- ✅ Algoritmos e estruturas de dados
- ✅ Banco de dados (SQL, modelagem ER)
- ✅ Sistemas operacionais (Linux, Windows)
- ✅ Redes (TCP/IP, protocolos, VLAN)
- ✅ Segurança da informação
- ✅ Noções de Informática (Excel, atalhos)
- ✅ Legislação (LGPD, Marco Civil)

## 🛠️ Stack Tecnológica

| Componente | Tecnologia |
|------------|-----------|
| Backend | FastAPI (Python 3.11) |
| Frontend | React 18 + Vite |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| Proxy | Nginx |
| Container | Docker + Docker Compose |
| CI/CD | GitHub Actions |

## 📖 Documentação

- 📘 [Quickstart Guide](docs/QUICKSTART.md) - Início rápido detalhado
- 📗 [API Documentation](docs/API.md) - Documentação completa da API
- 📙 [Architecture](docs/ARCHITECTURE.md) - Arquitetura do sistema
- 📕 [Deployment Guide](docs/DEPLOYMENT.md) - Guia de deploy
- 📔 [FAQ](docs/FAQ.md) - Perguntas frequentes
- 📓 [Testing Guide](TESTING.md) - Guia de testes

## 🧪 Testes

```bash
# Backend
docker-compose exec api pytest tests/ -v --cov=.

# Frontend
docker-compose exec web npm test

# Validação de questões
docker-compose exec api python scripts/validate_questions.py
```

## 🚢 Deploy

### Opção 1: VPS (Recomendado)
```bash
# Em servidor Ubuntu 22.04+
git clone <repo>
cd simulados-ibgp
cp .env.example .env
# Edite .env para produção
docker-compose up -d
```

### Opção 2: Cloud Run (Google Cloud)
```bash
gcloud run deploy simulados-api --image ghcr.io/user/simulados-api
gcloud run deploy simulados-web --image ghcr.io/user/simulados-web
```

Veja [DEPLOYMENT.md](docs/DEPLOYMENT.md) para mais opções.

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para guidelines.

### Como Contribuir
1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m "Add: nova funcionalidade"`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📊 Status do Projeto

- ✅ Ingestão de editais
- ✅ Geração de questões
- ✅ Validação QA
- ✅ Simulados configuráveis
- ✅ Treino adaptativo (SRS)
- ✅ Analytics completo
- ✅ Export de dados
- ✅ API REST completa
- ✅ Frontend React
- ✅ Autenticação JWT
- ✅ Containerização
- ✅ CI/CD
- ✅ Documentação completa
- ✅ Testes automatizados

## 🎯 Roadmap

### Curto Prazo
- [ ] Rate limiting
- [ ] Websockets para simulados em tempo real
- [ ] PWA (Progressive Web App)

### Médio Prazo
- [ ] Gamificação avançada
- [ ] Suporte a mais bancas
- [ ] Machine Learning para geração de questões

### Longo Prazo
- [ ] Análise preditiva de desempenho
- [ ] Comunidade de questões
- [ ] Mobile apps (iOS/Android)

## 📄 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

## 🙏 Agradecimentos

Sistema desenvolvido para auxiliar candidatos a concursos públicos na área de Tecnologia da Informação.

## 📞 Suporte

- 🐛 [Reportar Bug](https://github.com/seu-usuario/simulados-ibgp/issues/new?template=bug_report.md)
- 💡 [Sugerir Funcionalidade](https://github.com/seu-usuario/simulados-ibgp/issues/new?template=feature_request.md)
- 💬 [Discussões](https://github.com/seu-usuario/simulados-ibgp/discussions)

## ⭐ Star History

Se este projeto foi útil, considere dar uma estrela! ⭐

---

**Versão**: 1.0.0 | **Status**: ✅ Pronto para Produção | **Última Atualização**: 26/01/2026
