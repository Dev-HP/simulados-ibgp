# Quickstart Guide

## Início Rápido (5 minutos)

### Pré-requisitos
- Docker e Docker Compose instalados
- Git

### Passo 1: Clone e Configure
```bash
git clone <repo-url>
cd simulados-ibgp
cp .env.example .env
```

### Passo 2: Inicie os Containers
```bash
docker-compose up --build
```

Aguarde até ver:
```
api_1  | INFO:     Application startup complete.
web_1  | VITE ready in 1234 ms
```

### Passo 3: Acesse a Aplicação
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

### Passo 4: Popule com Dados de Teste
```bash
docker-compose exec api python scripts/seed_database.py
```

### Passo 5: Teste o Sistema

#### 5.1 Faça Login
- Usuário: `teste`
- Senha: `senha123`

#### 5.2 Upload de Edital
1. Vá para "Upload Edital"
2. Selecione `data/pasted_content.txt`
3. Clique em "Upload"
4. Aguarde: "Conteúdo programático recebido"

#### 5.3 Crie um Simulado
1. Vá para "Simulados"
2. Clique em "Criar Simulado"
3. Preencha:
   - Nome: "Meu Primeiro Simulado"
   - Questões: 10
   - Tempo: 30 minutos
4. Clique em "Criar"

#### 5.4 Execute o Simulado
1. Clique em "Iniciar" no simulado criado
2. Responda as questões
3. Veja o feedback imediato
4. Finalize e veja o relatório

## Comandos Úteis

### Ver Logs
```bash
# Todos os serviços
docker-compose logs -f

# Apenas API
docker-compose logs -f api

# Apenas Web
docker-compose logs -f web
```

### Parar os Containers
```bash
docker-compose down
```

### Rebuild Completo
```bash
docker-compose down -v
docker-compose up --build
```

### Acessar Shell do Container
```bash
# API (Python)
docker-compose exec api bash

# Web (Node)
docker-compose exec web sh

# PostgreSQL
docker-compose exec postgres psql -U simulados_user simulados_db
```

### Executar Testes
```bash
# API
docker-compose exec api pytest tests/ -v

# Web
docker-compose exec web npm test
```

### Validar Questões
```bash
docker-compose exec api python scripts/validate_questions.py
```

## Troubleshooting

### Porta já em uso
Edite `docker-compose.yml` e altere as portas:
```yaml
ports:
  - "8001:8000"  # API
  - "3001:3000"  # Web
```

### Erro de conexão com banco
```bash
# Verificar status
docker-compose ps

# Reiniciar PostgreSQL
docker-compose restart postgres

# Ver logs
docker-compose logs postgres
```

### Container não inicia
```bash
# Limpar tudo e reconstruir
docker-compose down -v
docker system prune -a
docker-compose up --build
```

### Erro de permissão
```bash
# Linux/Mac
sudo chown -R $USER:$USER .

# Windows
# Execute Docker Desktop como Administrador
```

## Próximos Passos

1. **Explore a API**: http://localhost:8000/docs
2. **Adicione mais questões**: Use a API ou edite `data/sample_questions.json`
3. **Customize**: Edite templates em `api/services/question_generator.py`
4. **Deploy**: Veja `docs/DEPLOYMENT.md`

## Recursos

- [Documentação da API](docs/API.md)
- [Arquitetura](docs/ARCHITECTURE.md)
- [Guia de Contribuição](CONTRIBUTING.md)
- [Deploy](docs/DEPLOYMENT.md)

## Suporte

- Issues: GitHub Issues
- Discussões: GitHub Discussions
- Email: [seu-email]

## Licença

MIT License - veja [LICENSE](LICENSE)
