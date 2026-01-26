# Arquitetura do Sistema

## Visão Geral

O Sistema de Simulados IBGP é uma aplicação full-stack containerizada com arquitetura de microserviços.

```
┌─────────────┐
│   Nginx     │  Reverse Proxy
└──────┬──────┘
       │
   ┌───┴────┐
   │        │
┌──▼──┐  ┌─▼────┐
│ Web │  │ API  │
│React│  │FastAPI│
└─────┘  └──┬───┘
            │
      ┌─────┴─────┐
      │           │
   ┌──▼──┐    ┌──▼──┐
   │ PG  │    │Redis│
   └─────┘    └─────┘
```

## Componentes

### 1. Frontend (React + Vite)
- **Tecnologia**: React 18, Vite, React Router
- **Responsabilidades**:
  - Interface do usuário
  - Upload de editais
  - Execução de simulados
  - Visualização de resultados e analytics
- **Porta**: 3000

### 2. Backend (FastAPI)
- **Tecnologia**: Python 3.11, FastAPI, SQLAlchemy
- **Responsabilidades**:
  - API REST
  - Parse de editais
  - Geração de questões
  - Lógica de simulados
  - Algoritmo adaptativo (SRS)
  - Validação QA
- **Porta**: 8000

### 3. Banco de Dados (PostgreSQL)
- **Tecnologia**: PostgreSQL 15
- **Responsabilidades**:
  - Armazenamento persistente
  - Usuários, questões, simulados, resultados
- **Porta**: 5432

### 4. Cache (Redis)
- **Tecnologia**: Redis 7
- **Responsabilidades**:
  - Cache de sessões
  - Fila de questões SRS
  - Rate limiting (futuro)
- **Porta**: 6379

### 5. Reverse Proxy (Nginx)
- **Tecnologia**: Nginx Alpine
- **Responsabilidades**:
  - Roteamento de requisições
  - Load balancing (futuro)
  - SSL termination
- **Porta**: 80/443

## Fluxo de Dados

### 1. Upload de Edital
```
User → Web → API → Parser → DB
                    ↓
                  Topics
```

### 2. Geração de Questões
```
Topics → Generator → QA Validator → DB
         ↓
      Templates
```

### 3. Execução de Simulado
```
User → Web → API → Simulado Service
                    ↓
                Questions (filtered)
                    ↓
                User Answers
                    ↓
                Feedback
```

### 4. Treino Adaptativo
```
User Performance → Adaptive Service → SRS Algorithm
                                      ↓
                                Priority Queue
                                      ↓
                                Review/New Questions
```

## Modelos de Dados

### Principais Entidades

1. **User**
   - Autenticação e perfil
   - Relacionamento: results, answers

2. **Syllabus**
   - Edital parseado
   - Estrutura hierárquica
   - Relacionamento: topics

3. **Topic**
   - Disciplina > Tópico > Subtópico
   - Referência ao edital
   - Relacionamento: questions

4. **Question**
   - Enunciado, alternativas, gabarito
   - Metadados (dificuldade, tempo, QA)
   - Relacionamento: answers

5. **Simulado**
   - Configuração do simulado
   - Relacionamento: questions, results

6. **SimuladoResult**
   - Resultado completo
   - Métricas e plano de estudo
   - Relacionamento: user, simulado

7. **UserAnswer**
   - Resposta individual
   - Tempo, tipo de erro
   - Relacionamento: user, question

## Serviços

### 1. SyllabusParser
- Parse hierárquico de editais
- Extração de PDF
- Detecção de disciplinas/tópicos

### 2. QuestionGenerator
- Geração baseada em templates
- Distribuição por tópico
- Aplicação de seeds

### 3. QAValidator
- Validação factual
- Verificação linguística
- Detecção de duplicidade
- Score de qualidade

### 4. SimuladoService
- Criação de simulados
- Seleção de questões
- Processamento de respostas
- Geração de relatórios

### 5. AdaptiveService
- Análise de desempenho
- Algoritmo SRS
- Priorização de tópicos
- Plano de estudo personalizado

### 6. ExportService
- Export GIFT (Moodle)
- Export CSV
- Export JSON

## Segurança

### Autenticação
- JWT Bearer tokens
- OAuth2 (Google) - opcional
- Hashing de senhas (bcrypt)

### Autorização
- Middleware de autenticação
- Proteção de rotas sensíveis

### Validação
- Pydantic schemas
- Sanitização de inputs
- Rate limiting (futuro)

## Performance

### Otimizações
- Índices no banco de dados
- Cache Redis para sessões
- Paginação de resultados
- Lazy loading no frontend

### Escalabilidade
- Containerização (Docker)
- Stateless API
- Horizontal scaling ready
- Load balancing (Nginx)

## Monitoramento

### Logs
- Structured logging
- Log levels (INFO, WARNING, ERROR)
- Rotação de logs

### Métricas (Futuro)
- Prometheus
- Grafana dashboards
- Alerting

## CI/CD

### Pipeline
1. **Test**: Pytest (API) + Vitest (Web)
2. **Lint**: Black, Flake8, ESLint
3. **Build**: Docker images
4. **Push**: GitHub Container Registry
5. **Deploy**: Automático (main branch)

### Ambientes
- **Development**: Local (docker-compose)
- **Staging**: Cloud (opcional)
- **Production**: VPS/Cloud

## Backup e Disaster Recovery

### Backup
- PostgreSQL: pg_dump diário
- Arquivos: rsync para storage
- Retenção: 30 dias

### Recovery
- Restore de backup
- Documentação de procedimentos
- Testes periódicos

## Roadmap Técnico

### Curto Prazo
- [ ] Rate limiting
- [ ] Websockets para simulados em tempo real
- [ ] PWA (Progressive Web App)

### Médio Prazo
- [ ] Microserviços separados
- [ ] Message queue (RabbitMQ/Kafka)
- [ ] Elasticsearch para busca

### Longo Prazo
- [ ] Machine Learning para geração de questões
- [ ] Análise preditiva de desempenho
- [ ] Gamificação avançada
