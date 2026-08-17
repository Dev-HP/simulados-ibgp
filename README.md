# Simulados IBGP

> Sistema de simulados adaptativos para preparação de Técnico em Informática, com frontend React, API FastAPI, banco PostgreSQL e geração/organização de questões.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Para quem é

O projeto foi criado para apoiar estudos para o concurso de Técnico em Informática da Câmara Municipal de Porto Velho/RO. Ele é um protótipo educacional: use dados e credenciais de demonstração, nunca informações pessoais de estudantes.

## Como experimentar

- **Frontend:** [simulados-ibgp-1.onrender.com](https://simulados-ibgp-1.onrender.com/)
- **API:** [documentação OpenAPI](https://simulados-ibgp.onrender.com/docs)

A tela inicial exige autenticação. Quando a instância de demonstração estiver ativa, use somente a conta de teste informada nas configurações do ambiente. Não reutilize a senha de demonstração em produção.

## Fluxo principal

1. O estudante acessa a aplicação e inicia um simulado.
2. A API entrega questões e registra respostas.
3. O sistema calcula desempenho e pode adaptar a próxima seleção de questões.
4. O usuário acompanha resultado e histórico.

Inclua screenshots do fluxo antes de divulgar o projeto como case completo: tela inicial, questão, resultado e painel de evolução.

## Stack

| Camada | Tecnologias |
|---|---|
| Backend | FastAPI, SQLAlchemy, PostgreSQL e Redis. |
| Frontend | React, Vite e TailwindCSS. |
| Conteúdo | Integração opcional com HuggingFace para geração/apoio às questões. |
| Operação | Docker, Render e scripts de teste/deploy. |

## Execução local

```bash
git clone https://github.com/Dev-HP/simulados-ibgp.git
cd simulados-ibgp

# Backend
cd api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload

# Em outro terminal, frontend
cd web
npm install
npm run dev
```

Preencha o `.env` com valores locais. Nunca publique chaves, senhas reais ou tokens no repositório.

## Testes

```bash
python test_final.py
cd api && pytest
python scripts/tests/test_complete_flow.py
```

## Estrutura

```text
api/       backend FastAPI, rotas, serviços e modelos
web/       frontend React
scripts/   utilitários de banco, deploy e testes
config/    Render, Docker Compose e Makefile
docs/      arquitetura, deploy e referência da API
data/      dados de exemplo
```

## Documentação

- [Arquitetura](docs/ARCHITECTURE.md)
- [Deploy](docs/DEPLOYMENT.md)
- [API](docs/API.md)
- [Quick start](QUICKSTART.md)
- [Status](STATUS.md)

## Licença

O projeto está sob a licença [MIT](LICENSE). Contribuições devem preservar a separação entre dados de demonstração e dados reais.

## Autor

**Hélio Paulo Leite de Lima** — [GitHub](https://github.com/Dev-HP)
