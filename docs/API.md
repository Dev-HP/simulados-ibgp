# Documentação da API

## Base URL
```
http://localhost:8000/api
```

## Autenticação
A API usa JWT Bearer tokens. Para obter um token:

```bash
POST /api/token
Content-Type: application/x-www-form-urlencoded

username=teste&password=senha123
```

Resposta:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

Use o token em requisições protegidas:
```bash
Authorization: Bearer eyJ...
```

## Endpoints

### 1. Upload de Edital

**POST /api/upload-syllabus**

Upload e parse de edital (TXT ou PDF).

**Request:**
```bash
curl -X POST http://localhost:8000/api/upload-syllabus \
  -F "file=@edital.txt"
```

**Response:**
```json
{
  "id": 1,
  "filename": "edital.txt",
  "parsed_structure": {
    "disciplinas": [...]
  },
  "uploaded_at": "2026-01-26T10:00:00",
  "message": "Conteúdo programático recebido"
}
```

### 2. Geração de Banco de Questões

**POST /api/generate-bank**

Gera banco de questões baseado nos tópicos do edital.

**Request:**
```json
{
  "seeds": ["seed1", "seed2"],
  "min_questions_per_topic": 10,
  "target_topics": ["Hardware", "Redes"]
}
```

**Response:**
```json
{
  "message": "Question bank generated successfully",
  "total_questions": 150,
  "topics_covered": 15
}
```

### 3. Listar Questões

**GET /api/questions**

Lista questões com filtros opcionais.

**Query Parameters:**
- `disciplina` (opcional): Filtrar por disciplina
- `topico` (opcional): Filtrar por tópico
- `dificuldade` (opcional): fácil, médio, difícil
- `skip` (opcional): Paginação
- `limit` (opcional): Limite de resultados

**Response:**
```json
[
  {
    "id": 1,
    "disciplina": "Hardware",
    "topico": "Memórias",
    "enunciado": "Sobre memórias RAM...",
    "alternativa_a": "...",
    "alternativa_b": "...",
    "alternativa_c": "...",
    "alternativa_d": "...",
    "gabarito": "A",
    "explicacao_detalhada": "...",
    "dificuldade": "médio",
    "qa_score": 95.0,
    "qa_status": "approved"
  }
]
```

### 4. Criar Simulado

**POST /api/create-simulado**

Cria simulado configurável.

**Request:**
```json
{
  "nome": "Simulado Oficial 1",
  "descricao": "Simulado completo",
  "numero_questoes": 40,
  "tempo_total": 120,
  "disciplinas": ["Hardware", "Redes", "Linux"],
  "dificuldade_alvo": "médio",
  "pesos": {
    "Hardware": 1.5,
    "Redes": 1.0
  },
  "aleatorizacao_por_topico": true
}
```

**Response:**
```json
{
  "id": 1,
  "nome": "Simulado Oficial 1",
  "numero_questoes": 40,
  "tempo_total": 120,
  "is_oficial": false,
  "created_at": "2026-01-26T10:00:00"
}
```

### 5. Executar Simulado

**GET /api/simulados/{simulado_id}**

Retorna simulado com questões.

**Response:**
```json
{
  "simulado": {...},
  "questions": [...]
}
```

### 6. Submeter Resposta

**POST /api/simulados/{simulado_id}/answer**

Submete resposta e retorna feedback imediato.

**Request:**
```json
{
  "question_id": 1,
  "resposta": "A",
  "tempo_resposta": 120
}
```

**Response:**
```json
{
  "is_correct": true,
  "gabarito": "A",
  "explicacao": "A alternativa A está correta...",
  "referencia": "Edital página 2",
  "tipo_erro": null,
  "questoes_similares": [2, 3, 4]
}
```

### 7. Finalizar Simulado

**POST /api/simulados/{simulado_id}/finalize**

Finaliza simulado e gera relatório completo.

**Response:**
```json
{
  "id": 1,
  "simulado_id": 1,
  "score": 75.5,
  "tempo_total": 3600,
  "acertos_por_disciplina": {
    "Hardware": {
      "total": 10,
      "acertos": 8,
      "percentual": 80
    }
  },
  "tempo_medio_questao": 90,
  "indice_confianca": 72.5,
  "plano_estudo": {
    "disciplinas_prioridade": ["Redes"],
    "tipos_erro_comuns": {"conceitual": 3},
    "recomendacoes": ["Revisar Redes"]
  }
}
```

### 8. Analytics do Usuário

**GET /api/analytics/{user_id}**

Retorna analytics completo do usuário.

**Response:**
```json
{
  "total_simulados": 5,
  "media_score": 78.5,
  "disciplinas_fortes": ["Hardware", "Linux"],
  "disciplinas_fracas": ["Redes"],
  "tempo_medio_questao": 95.5,
  "progresso_temporal": [
    {"data": "2026-01-20", "score": 70},
    {"data": "2026-01-25", "score": 78.5}
  ]
}
```

### 9. Sugestões de Estudo (Adaptativo)

**POST /api/suggestions**

Retorna plano de estudo adaptativo (SRS).

**Response:**
```json
{
  "performance_summary": {...},
  "priority_topics": [
    {
      "disciplina": "Redes",
      "topico": "Protocolos",
      "taxa_acerto": 45.5,
      "prioridade": 85.2
    }
  ],
  "review_questions": [1, 5, 8],
  "new_questions": [15, 20, 25],
  "daily_goal": {
    "review": 10,
    "new": 10
  }
}
```

## Códigos de Status

- `200 OK`: Sucesso
- `201 Created`: Recurso criado
- `400 Bad Request`: Requisição inválida
- `401 Unauthorized`: Não autenticado
- `404 Not Found`: Recurso não encontrado
- `500 Internal Server Error`: Erro no servidor

## Rate Limiting

Atualmente não há rate limiting implementado. Em produção, considere adicionar.

## Swagger/OpenAPI

Documentação interativa disponível em:
```
http://localhost:8000/docs
```
