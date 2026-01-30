# 🎯 Sistema de Simulados IBGP

Sistema de simulados adaptativos para concurso de Técnico em Informática - Câmara Municipal de Porto Velho/RO.

## 🚀 Quick Start

### Desenvolvimento Local

```bash
# 1. Instalar dependências
cd api && pip install -r requirements.txt
cd ../web && npm install

# 2. Configurar .env
cp .env.example .env
# Editar .env com suas credenciais

# 3. Iniciar backend
cd api && uvicorn main:app --reload

# 4. Iniciar frontend
cd web && npm run dev
```

### Deploy Render

```bash
# Deploy automático via GitHub
git push origin main

# Ou manual
python scripts/deploy/deploy_render.bat
```

## 📁 Estrutura do Projeto

```
├── api/                    # Backend FastAPI
│   ├── routers/           # Endpoints da API
│   ├── services/          # Lógica de negócio
│   ├── models.py          # Modelos do banco
│   └── main.py            # App principal
│
├── web/                    # Frontend React
│   ├── src/
│   │   ├── pages/         # Páginas
│   │   └── App.jsx        # App principal
│   └── vite.config.js
│
├── scripts/               # Scripts utilitários
│   ├── deploy/           # Scripts de deploy
│   ├── database/         # Scripts de banco
│   └── tests/            # Scripts de teste
│
├── config/                # Arquivos de configuração
│   ├── render.yaml       # Config Render
│   ├── docker-compose.yml
│   └── Makefile
│
├── docs/                  # Documentação
├── data/                  # Dados de exemplo
├── output/               # Arquivos gerados
│
├── test_final.py         # Teste principal
├── init_database.py      # Inicializar banco
├── README.md             # Este arquivo
├── QUICKSTART.md         # Início rápido
└── STATUS.md             # Status do sistema
```

## 🔑 Variáveis de Ambiente

### Obrigatórias

```env
# HuggingFace (geração de questões)
HUGGINGFACE_API_KEY=hf_your_key_here

# Database
POSTGRES_HOST=localhost
POSTGRES_DB=simulados_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password

# JWT
SECRET_KEY=your_secret_key_here
```

### Opcionais

```env
# Redis (cache)
REDIS_HOST=localhost
REDIS_PORT=6379
```

## 🧪 Testes

```bash
# Teste completo do sistema
python test_final.py

# Testes unitários
cd api && pytest

# Teste de integração
python scripts/tests/test_complete_flow.py
```

## 📚 Documentação

- **API**: https://simulados-ibgp.onrender.com/docs
- **Arquitetura**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Deploy**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **API Reference**: [docs/API.md](docs/API.md)

## 🛠️ Tecnologias

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- HuggingFace API

### Frontend
- React
- Vite
- TailwindCSS

## 🔗 Links

- **Produção**: https://simulados-ibgp.onrender.com
- **Frontend**: https://simulados-ibgp-1.onrender.com
- **GitHub**: https://github.com/Dev-HP/simulados-ibgp

## 📝 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 👥 Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para guidelines.
