# 📑 Índice Completo - Sistema de Simulados IBGP

## 🎯 Comece Aqui

- **[START_HERE.md](START_HERE.md)** ⭐ - Ponto de partida recomendado
- **[RESUMO_FINAL.txt](RESUMO_FINAL.txt)** - Resumo executivo em texto
- **[README.md](README.md)** - Documentação principal do projeto

---

## 🚀 Guias de Deploy

### Passo a Passo
- **[INSTRUCOES_COMPLETAS.md](INSTRUCOES_COMPLETAS.md)** ⭐⭐⭐ - Guia completo e detalhado
- **[DEPLOY_RAPIDO.md](DEPLOY_RAPIDO.md)** ⭐⭐ - Deploy em 3 passos
- **[GITHUB_SETUP.md](GITHUB_SETUP.md)** ⭐ - GitHub + todas as opções de deploy

### Scripts Automáticos
- **[setup_github.bat](setup_github.bat)** - Script Windows
- **[setup_github.sh](setup_github.sh)** - Script Linux/Mac
- **[verify_system.sh](verify_system.sh)** - Verificar sistema

---

## 📚 Documentação Principal

### Visão Geral
- **[README.md](README.md)** - Documentação principal
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Resumo completo do projeto
- **[EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)** - Resumo executivo
- **[CHECKLIST.md](CHECKLIST.md)** - Checklist de verificação

### Documentação Técnica
- **[docs/API.md](docs/API.md)** - Documentação completa da API
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Arquitetura do sistema
- **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Opções de deploy
- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** - Início rápido local
- **[docs/FAQ.md](docs/FAQ.md)** - Perguntas frequentes

---

## 🛠️ Desenvolvimento

### Contribuição
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guia de contribuição
- **[TESTING.md](TESTING.md)** - Guia de testes
- **[CHANGELOG.md](CHANGELOG.md)** - Histórico de mudanças
- **[LICENSE](LICENSE)** - Licença MIT

### Configuração
- **[.env.example](.env.example)** - Variáveis de ambiente
- **[docker-compose.yml](docker-compose.yml)** - Orquestração Docker
- **[Makefile](Makefile)** - Comandos úteis

---

## 🐳 Docker

### Dockerfiles
- **[docker/Dockerfile.api](docker/Dockerfile.api)** - Backend
- **[docker/Dockerfile.web](docker/Dockerfile.web)** - Frontend

### Infraestrutura
- **[infra/nginx.conf](infra/nginx.conf)** - Configuração Nginx
- **[api/db/init.sql](api/db/init.sql)** - Inicialização do banco

---

## 💻 Backend (API)

### Core
- **[api/main.py](api/main.py)** - Aplicação principal
- **[api/models.py](api/models.py)** - Modelos SQLAlchemy
- **[api/schemas.py](api/schemas.py)** - Schemas Pydantic
- **[api/database.py](api/database.py)** - Configuração do banco
- **[api/auth.py](api/auth.py)** - Autenticação JWT
- **[api/requirements.txt](api/requirements.txt)** - Dependências

### Routers (Endpoints)
- **[api/routers/syllabus.py](api/routers/syllabus.py)** - Upload de editais
- **[api/routers/questions.py](api/routers/questions.py)** - Questões
- **[api/routers/simulados.py](api/routers/simulados.py)** - Simulados
- **[api/routers/users.py](api/routers/users.py)** - Usuários
- **[api/routers/analytics.py](api/routers/analytics.py)** - Analytics
- **[api/routers/export.py](api/routers/export.py)** - Export de dados

### Services (Lógica de Negócio)
- **[api/services/parser.py](api/services/parser.py)** - Parse de editais
- **[api/services/question_generator.py](api/services/question_generator.py)** - Geração de questões
- **[api/services/qa_validator.py](api/services/qa_validator.py)** - Validação QA
- **[api/services/simulado_service.py](api/services/simulado_service.py)** - Lógica de simulados
- **[api/services/adaptive_service.py](api/services/adaptive_service.py)** - Algoritmo SRS
- **[api/services/export_service.py](api/services/export_service.py)** - Export

### Scripts
- **[api/scripts/seed_database.py](api/scripts/seed_database.py)** - Popular banco
- **[api/scripts/validate_questions.py](api/scripts/validate_questions.py)** - Validar questões

### Testes
- **[api/tests/test_parser.py](api/tests/test_parser.py)** - Testes do parser
- **[api/tests/test_qa_validator.py](api/tests/test_qa_validator.py)** - Testes QA
- **[api/tests/test_simulado_service.py](api/tests/test_simulado_service.py)** - Testes simulados
- **[api/tests/conftest.py](api/tests/conftest.py)** - Fixtures pytest

### Configuração
- **[api/.flake8](api/.flake8)** - Configuração Flake8
- **[api/pyproject.toml](api/pyproject.toml)** - Black/MyPy
- **[api/pytest.ini](api/pytest.ini)** - Pytest

---

## 🎨 Frontend (Web)

### Core
- **[web/src/main.jsx](web/src/main.jsx)** - Entry point
- **[web/src/App.jsx](web/src/App.jsx)** - App principal
- **[web/src/index.css](web/src/index.css)** - Estilos globais
- **[web/index.html](web/index.html)** - HTML base

### Páginas
- **[web/src/pages/Home.jsx](web/src/pages/Home.jsx)** - Página inicial
- **[web/src/pages/Upload.jsx](web/src/pages/Upload.jsx)** - Upload de editais
- **[web/src/pages/Simulados.jsx](web/src/pages/Simulados.jsx)** - Lista de simulados
- **[web/src/pages/SimuladoExec.jsx](web/src/pages/SimuladoExec.jsx)** - Executar simulado
- **[web/src/pages/Results.jsx](web/src/pages/Results.jsx)** - Resultados
- **[web/src/pages/Analytics.jsx](web/src/pages/Analytics.jsx)** - Analytics

### Configuração
- **[web/package.json](web/package.json)** - Dependências
- **[web/vite.config.js](web/vite.config.js)** - Configuração Vite
- **[web/.eslintrc.cjs](web/.eslintrc.cjs)** - ESLint

---

## 📊 Dados

### Editais
- **[data/pasted_content.txt](data/pasted_content.txt)** - Edital de exemplo
- **[data/editais/](data/editais/)** - Diretório para editais

### Questões
- **[data/sample_questions.json](data/sample_questions.json)** - 10 questões de exemplo

### Uploads
- **[data/uploads/](data/uploads/)** - Diretório para uploads

---

## 🔄 CI/CD

### GitHub Actions
- **[.github/workflows/ci.yml](.github/workflows/ci.yml)** - Pipeline CI/CD

### Templates
- **[.github/ISSUE_TEMPLATE/bug_report.md](.github/ISSUE_TEMPLATE/bug_report.md)** - Bug report
- **[.github/ISSUE_TEMPLATE/feature_request.md](.github/ISSUE_TEMPLATE/feature_request.md)** - Feature request
- **[.github/ISSUE_TEMPLATE/dados_edital.md](.github/ISSUE_TEMPLATE/dados_edital.md)** - Dados de edital
- **[.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md)** - Pull request

---

## 📁 Estrutura Completa

```
simulados-ibgp/
├── 📄 Documentação Principal
│   ├── START_HERE.md ⭐
│   ├── README.md
│   ├── PROJECT_SUMMARY.md
│   ├── EXECUTIVE_SUMMARY.md
│   └── INDICE.md (este arquivo)
│
├── 🚀 Guias de Deploy
│   ├── INSTRUCOES_COMPLETAS.md ⭐⭐⭐
│   ├── DEPLOY_RAPIDO.md ⭐⭐
│   ├── GITHUB_SETUP.md ⭐
│   ├── setup_github.bat
│   └── setup_github.sh
│
├── 📚 Documentação Técnica
│   ├── docs/API.md
│   ├── docs/ARCHITECTURE.md
│   ├── docs/DEPLOYMENT.md
│   ├── docs/QUICKSTART.md
│   └── docs/FAQ.md
│
├── 🛠️ Desenvolvimento
│   ├── CONTRIBUTING.md
│   ├── TESTING.md
│   ├── CHANGELOG.md
│   └── CHECKLIST.md
│
├── 💻 Backend (api/)
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   ├── services/
│   ├── tests/
│   └── scripts/
│
├── 🎨 Frontend (web/)
│   ├── src/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
│
├── 🐳 Docker
│   ├── docker-compose.yml
│   ├── docker/
│   └── infra/
│
├── 📊 Dados
│   ├── data/pasted_content.txt
│   ├── data/sample_questions.json
│   └── data/editais/
│
└── 🔄 CI/CD
    └── .github/
        ├── workflows/
        └── ISSUE_TEMPLATE/
```

---

## 🎯 Navegação Rápida

### Para Iniciantes
1. [START_HERE.md](START_HERE.md)
2. [INSTRUCOES_COMPLETAS.md](INSTRUCOES_COMPLETAS.md)
3. [docs/QUICKSTART.md](docs/QUICKSTART.md)

### Para Deploy
1. [DEPLOY_RAPIDO.md](DEPLOY_RAPIDO.md)
2. [GITHUB_SETUP.md](GITHUB_SETUP.md)
3. [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

### Para Desenvolvedores
1. [CONTRIBUTING.md](CONTRIBUTING.md)
2. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
3. [docs/API.md](docs/API.md)
4. [TESTING.md](TESTING.md)

### Para Entender o Sistema
1. [README.md](README.md)
2. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
3. [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)

---

## 📞 Suporte

- **FAQ**: [docs/FAQ.md](docs/FAQ.md)
- **Issues**: GitHub Issues
- **Discussões**: GitHub Discussions

---

## ⭐ Arquivos Mais Importantes

1. **[START_HERE.md](START_HERE.md)** - Comece aqui!
2. **[INSTRUCOES_COMPLETAS.md](INSTRUCOES_COMPLETAS.md)** - Guia completo
3. **[README.md](README.md)** - Documentação principal
4. **[docker-compose.yml](docker-compose.yml)** - Orquestração
5. **[api/main.py](api/main.py)** - Backend principal
6. **[web/src/App.jsx](web/src/App.jsx)** - Frontend principal

---

**Total de arquivos**: 85+
**Linhas de documentação**: 2000+
**Guias disponíveis**: 15+

---

Navegue pelos arquivos acima para encontrar o que precisa!
