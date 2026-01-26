# Guia de Testes

## Testes Automatizados

### Backend (API)

#### Executar Todos os Testes
```bash
docker-compose exec api pytest tests/ -v
```

#### Com Cobertura
```bash
docker-compose exec api pytest tests/ -v --cov=. --cov-report=html
```

#### Testes Específicos
```bash
# Apenas validador QA
docker-compose exec api pytest tests/test_qa_validator.py -v

# Apenas parser
docker-compose exec api pytest tests/test_parser.py -v

# Apenas simulados
docker-compose exec api pytest tests/test_simulado_service.py -v
```

#### Testes Lentos
```bash
docker-compose exec api pytest tests/ -v -m "not slow"
```

### Frontend (Web)

#### Executar Testes
```bash
docker-compose exec web npm test
```

#### Com Watch Mode
```bash
docker-compose exec web npm test -- --watch
```

## Testes Manuais

### 1. Upload de Edital

**Objetivo**: Verificar ingestão e parse de editais

**Passos**:
1. Acesse http://localhost:3000/upload
2. Selecione `data/pasted_content.txt`
3. Clique em "Upload"

**Resultado Esperado**:
- Mensagem: "Conteúdo programático recebido"
- Status 200
- Estrutura parseada visível

**Teste via API**:
```bash
curl -X POST http://localhost:8000/api/upload-syllabus \
  -F "file=@data/pasted_content.txt"
```

### 2. Geração de Banco de Questões

**Objetivo**: Verificar geração automática de questões

**Passos**:
1. Após upload do edital
2. POST `/api/generate-bank`

**Resultado Esperado**:
- Mínimo 10 questões por tópico
- Questões com QA score >= 60
- Todas as disciplinas cobertas

**Teste via API**:
```bash
curl -X POST http://localhost:8000/api/generate-bank \
  -H "Content-Type: application/json" \
  -d '{"min_questions_per_topic": 10}'
```

### 3. Validação de Questões

**Objetivo**: Verificar qualidade das questões

**Passos**:
```bash
docker-compose exec api python scripts/validate_questions.py
```

**Resultado Esperado**:
- Score de cada questão
- Status (approved/review_required/rejected)
- Lista de issues se houver

### 4. Criação de Simulado

**Objetivo**: Verificar criação de simulados configuráveis

**Passos**:
1. Acesse http://localhost:3000/simulados
2. Clique em "Criar Simulado"
3. Preencha:
   - Nome: "Teste"
   - Questões: 10
   - Tempo: 30 min
4. Clique em "Criar"

**Resultado Esperado**:
- Simulado criado com ID
- 10 questões selecionadas
- Distribuição por tópicos

**Teste via API**:
```bash
curl -X POST http://localhost:8000/api/create-simulado \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Teste",
    "numero_questoes": 10,
    "tempo_total": 30
  }'
```

### 5. Execução de Simulado

**Objetivo**: Verificar fluxo completo de simulado

**Passos**:
1. Acesse simulado criado
2. Responda questões
3. Veja feedback imediato
4. Finalize simulado

**Resultado Esperado**:
- Feedback após cada resposta
- Explicação detalhada
- Questões similares sugeridas
- Relatório final completo

**Teste via API**:
```bash
# Submeter resposta
curl -X POST http://localhost:8000/api/simulados/1/answer \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "question_id": 1,
    "resposta": "A",
    "tempo_resposta": 120
  }'

# Finalizar
curl -X POST http://localhost:8000/api/simulados/1/finalize \
  -H "Authorization: Bearer <token>"
```

### 6. Analytics

**Objetivo**: Verificar métricas e analytics

**Passos**:
1. Acesse http://localhost:3000/analytics
2. Veja métricas do usuário

**Resultado Esperado**:
- Total de simulados
- Média de score
- Disciplinas fortes/fracas
- Progresso temporal

**Teste via API**:
```bash
curl -X GET http://localhost:8000/api/analytics/1 \
  -H "Authorization: Bearer <token>"
```

### 7. Treino Adaptativo

**Objetivo**: Verificar algoritmo SRS

**Passos**:
```bash
curl -X POST http://localhost:8000/api/suggestions \
  -H "Authorization: Bearer <token>"
```

**Resultado Esperado**:
- Tópicos prioritários (taxa < 60%)
- Questões para revisão
- Novas questões
- Meta diária

### 8. Export de Dados

**Objetivo**: Verificar export em múltiplos formatos

**Passos**:
```bash
# GIFT
curl -X GET http://localhost:8000/api/export/gift?disciplina=Hardware

# CSV
curl -X GET http://localhost:8000/api/export/csv?disciplina=Redes

# JSON
curl -X GET http://localhost:8000/api/export/json
```

**Resultado Esperado**:
- Arquivo no formato correto
- Todas as questões incluídas
- Metadados preservados

## Testes de Integração

### Fluxo Completo

**Objetivo**: Testar fluxo end-to-end

**Passos**:
1. Registrar usuário
2. Fazer login
3. Upload edital
4. Gerar banco
5. Criar simulado
6. Executar simulado
7. Ver analytics
8. Obter sugestões
9. Export dados

**Script de Teste**:
```bash
#!/bin/bash

# 1. Registrar
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@example.com",
    "username": "teste",
    "password": "senha123"
  }'

# 2. Login
TOKEN=$(curl -X POST http://localhost:8000/api/token \
  -d "username=teste&password=senha123" | jq -r .access_token)

# 3. Upload edital
curl -X POST http://localhost:8000/api/upload-syllabus \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@data/pasted_content.txt"

# 4. Gerar banco
curl -X POST http://localhost:8000/api/generate-bank \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"min_questions_per_topic": 10}'

# 5. Criar simulado
SIMULADO_ID=$(curl -X POST http://localhost:8000/api/create-simulado \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Teste Completo",
    "numero_questoes": 5,
    "tempo_total": 15
  }' | jq -r .id)

# 6. Ver analytics
curl -X GET http://localhost:8000/api/analytics/1 \
  -H "Authorization: Bearer $TOKEN"

echo "✅ Fluxo completo testado com sucesso!"
```

## Testes de Performance

### Load Testing

**Objetivo**: Verificar performance sob carga

**Ferramenta**: Apache Bench ou k6

```bash
# Instalar Apache Bench
sudo apt install apache2-utils

# Teste de carga
ab -n 1000 -c 10 http://localhost:8000/api/questions

# Resultado esperado:
# - Requests per second > 100
# - Time per request < 100ms
# - Failed requests = 0
```

### Stress Testing

```bash
# k6 script
k6 run --vus 50 --duration 30s stress-test.js
```

## Testes de Segurança

### 1. SQL Injection

**Teste**:
```bash
curl -X GET "http://localhost:8000/api/questions?disciplina=Hardware' OR '1'='1"
```

**Resultado Esperado**: Sem vulnerabilidade (SQLAlchemy protege)

### 2. XSS

**Teste**: Inserir script em questão
```bash
curl -X POST http://localhost:8000/api/questions \
  -H "Content-Type: application/json" \
  -d '{
    "enunciado": "<script>alert(1)</script>",
    ...
  }'
```

**Resultado Esperado**: Script escapado ou rejeitado

### 3. CSRF

**Teste**: Requisição sem token
```bash
curl -X POST http://localhost:8000/api/create-simulado \
  -H "Content-Type: application/json" \
  -d '{...}'
```

**Resultado Esperado**: 401 Unauthorized

## Checklist de Testes

### Antes de Commit
- [ ] Testes unitários passam
- [ ] Lint sem erros
- [ ] Cobertura >= 80%
- [ ] Documentação atualizada

### Antes de Deploy
- [ ] Testes de integração passam
- [ ] Testes manuais executados
- [ ] Performance aceitável
- [ ] Segurança verificada
- [ ] Backup testado
- [ ] Rollback planejado

## Relatórios

### Cobertura de Testes
```bash
docker-compose exec api pytest --cov=. --cov-report=html
# Ver em: htmlcov/index.html
```

### Relatório de Lint
```bash
docker-compose exec api flake8 . --format=html --htmldir=flake-report
```

## Troubleshooting de Testes

### Testes Falhando

1. **Limpar banco de teste**:
```bash
rm api/test.db
```

2. **Rebuild containers**:
```bash
docker-compose down -v
docker-compose up --build
```

3. **Ver logs detalhados**:
```bash
docker-compose exec api pytest tests/ -v -s
```

### Performance Ruim

1. **Verificar recursos**:
```bash
docker stats
```

2. **Otimizar queries**:
```bash
# Habilitar SQL logging
export SQLALCHEMY_ECHO=true
```

3. **Adicionar índices**:
```sql
CREATE INDEX idx_questions_disciplina ON questions(disciplina);
```

## Continuous Testing

### GitHub Actions

O pipeline CI/CD executa automaticamente:
- Testes unitários
- Testes de integração
- Lint
- Build
- Deploy (se main branch)

Ver: `.github/workflows/ci.yml`

## Métricas de Qualidade

### Objetivos
- Cobertura de testes: >= 80%
- Testes passando: 100%
- Lint errors: 0
- Performance: < 100ms por request
- Disponibilidade: >= 99%

### Monitoramento
- Logs: `docker-compose logs -f`
- Métricas: Prometheus (futuro)
- Alertas: Grafana (futuro)
