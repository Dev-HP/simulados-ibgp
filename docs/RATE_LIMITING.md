# 🛡️ Rate Limiting - Gemini API Free Tier

Sistema de controle de uso da API Gemini para garantir que permaneça dentro dos limites gratuitos.

## 📊 Limites do Free Tier

O Gemini Pro oferece um tier gratuito com os seguintes limites:

- **60 requisições por minuto**
- **1.500 requisições por dia**

## 🔒 Como Funciona

### 1. Rate Limiter

O sistema implementa um rate limiter que:

✅ Rastreia todas as requisições feitas
✅ Bloqueia requisições que excedem os limites
✅ Fornece mensagens claras sobre o tempo de espera
✅ Mantém estatísticas de uso

### 2. Margem de Segurança

Para evitar problemas, o sistema usa margens de segurança:

- **Limite por minuto**: 55 requisições (ao invés de 60)
- **Limite diário**: 1.400 requisições (ao invés de 1.500)

### 3. Bloqueio Automático

Quando um limite é atingido:

```
❌ Limite de 55 requisições/minuto atingido. Aguarde 45s.
```

ou

```
❌ Limite diário de 1.400 requisições atingido. Aguarde 8h.
```

## 📈 Monitoramento

### Endpoint de Estatísticas

```
GET /api/gemini-stats
```

Retorna:

```json
{
  "status": "ok",
  "tier": "free",
  "limits": {
    "per_minute": 55,
    "per_day": 1400
  },
  "usage": {
    "last_minute": 12,
    "today": 345,
    "total": 1250,
    "blocked": 5
  },
  "remaining": {
    "minute": 43,
    "day": 1055
  },
  "percentage": {
    "minute": 21.82,
    "day": 24.64
  },
  "warnings": [
    null,
    null
  ]
}
```

### Interface Visual

O frontend mostra em tempo real:

- 📊 Uso por minuto (barra de progresso)
- 📊 Uso diário (barra de progresso)
- ⚠️ Avisos quando próximo do limite
- 🚫 Requisições bloqueadas

## 💡 Estratégias de Uso

### 1. Geração em Lote

Ao invés de gerar 1 questão por vez, gere em lotes:

```
✅ Gerar 10 questões de uma vez
❌ Gerar 1 questão 10 vezes
```

**Por quê?**
- 1 requisição gera múltiplas questões
- Mais eficiente
- Economiza limite

### 2. Horários de Pico

Evite gerar questões em horários de pico:

- ❌ Durante aulas/simulados
- ✅ Madrugada/fim de semana
- ✅ Preparação prévia

### 3. Cache de Questões

O sistema já salva questões geradas:

- ✅ Importe questões reais primeiro
- ✅ Gere questões com antecedência
- ✅ Reutilize questões existentes

### 4. Priorização

Priorize geração para:

1. Tópicos sem questões
2. Tópicos com poucas questões
3. Tópicos mais importantes

## 📊 Estimativas de Uso

### Cenário 1: Uso Moderado

```
- 10 questões/dia
- 1 requisição por geração
- Total: 10 requisições/dia
- Duração: 140 dias no free tier
```

### Cenário 2: Uso Intenso

```
- 100 questões/dia
- 10 requisições (10 questões cada)
- Total: 10 requisições/dia
- Duração: 140 dias no free tier
```

### Cenário 3: Preparação Inicial

```
- 1000 questões em 1 dia
- 100 requisições (10 questões cada)
- Total: 100 requisições
- Sobram: 1300 requisições no dia
```

## ⚠️ Avisos e Alertas

### Aviso Amarelo (80% do limite)

```
⚠️ Limite por minuto atingido
```

**Ação**: Aguarde alguns segundos antes de continuar

### Aviso Vermelho (100% do limite)

```
🚫 Limite diário de 1.400 requisições atingido. Aguarde 8h.
```

**Ação**: Aguarde reset do limite ou use questões existentes

## 🔧 Configuração

### Ajustar Limites

Edite `api/services/rate_limiter.py`:

```python
gemini_rate_limiter = RateLimiter(
    requests_per_minute=55,  # Ajustar aqui
    requests_per_day=1400    # Ajustar aqui
)
```

### Desabilitar Rate Limiting (NÃO RECOMENDADO)

```python
# Em gemini_generator.py, comentar:
# can_make, error_msg = gemini_rate_limiter.can_make_request()
# if not can_make:
#     raise HTTPException(status_code=429, detail=error_msg)
```

⚠️ **Atenção**: Desabilitar pode resultar em:
- Bloqueio da API pelo Google
- Cobrança inesperada
- Perda de acesso

## 📈 Upgrade para Tier Pago

Se precisar de mais requisições:

### Gemini Pro (Pago)

- **Custo**: ~$0.00025 por requisição
- **Limite**: Muito maior
- **Exemplo**: 10.000 questões = ~$2.50

### Como Fazer Upgrade

1. Acesse: https://console.cloud.google.com/
2. Ative billing no projeto
3. Configure limites de gasto
4. Atualize a chave da API

## 🎯 Melhores Práticas

### ✅ Fazer

- Importar questões reais primeiro
- Gerar em lotes (10-20 questões)
- Monitorar uso regularmente
- Planejar geração com antecedência
- Usar cache de questões

### ❌ Evitar

- Gerar 1 questão por vez
- Ignorar avisos de limite
- Gerar durante horário de pico
- Regenerar questões existentes
- Desabilitar rate limiting

## 📊 Dashboard de Monitoramento

O frontend mostra:

```
🤖 Status da API Gemini (Free Tier)

┌─────────────────────────────┐
│ Limite por Minuto           │
│ 43 / 55                     │
│ ████████░░░░░░░░░░ 21.82%  │
│ 12 requisições no último    │
│ minuto                      │
└─────────────────────────────┘

┌─────────────────────────────┐
│ Limite Diário               │
│ 1055 / 1400                 │
│ ████░░░░░░░░░░░░░░ 24.64%  │
│ 345 requisições hoje        │
└─────────────────────────────┘
```

## 🆘 Troubleshooting

### Erro: "Rate limit exceeded"

**Causa**: Muitas requisições em pouco tempo

**Solução**:
1. Aguarde o tempo indicado
2. Reduza quantidade de questões
3. Gere em horários diferentes

### Erro: "Daily limit reached"

**Causa**: Limite diário atingido

**Solução**:
1. Aguarde reset (meia-noite UTC)
2. Use questões já geradas
3. Considere upgrade para tier pago

### Estatísticas não aparecem

**Causa**: Endpoint não configurado

**Solução**:
```bash
# Verificar se endpoint existe
curl http://localhost:8000/api/gemini-stats
```

## 📚 Recursos

- [Gemini API Pricing](https://ai.google.dev/pricing)
- [Rate Limits Documentation](https://ai.google.dev/docs/rate_limits)
- [Google Cloud Console](https://console.cloud.google.com/)
