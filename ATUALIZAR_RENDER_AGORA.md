# 🚨 AÇÃO IMEDIATA: ATUALIZAR RENDER

## API KEY CONFIGURADA LOCALMENTE ✅
- API Key: `[CHAVE_REVOGADA_POR_SEGURANCA]`
- Modelo: Fallback automático (Flash Lite → Flash → Pro)
- Rate Limit: Conservador (10/min, 100/dia)

## AGORA VOCÊ PRECISA FAZER:

### 1. Acessar Render Dashboard
```
https://dashboard.render.com
```

### 2. Encontrar o Serviço
- Clique em "simulados-ibgp" (API service)

### 3. Atualizar Environment Variable
- Settings → Environment
- Encontre: `GEMINI_API_KEY`
- Clique "Edit"
- Cole: `[NOVA_CHAVE_AQUI]`
- Clique "Save Changes"

### 4. Aguardar Redeploy
- Render fará redeploy automático (2-3 min)
- Aguarde até aparecer "Live"

### 5. Testar
```bash
python testar_endpoint_direto.py
```

## MELHORIAS IMPLEMENTADAS:
✅ Fallback automático entre modelos Gemini
✅ Rate limiting conservador
✅ Retry com backoff exponencial
✅ Tratamento robusto de erros
✅ Logs detalhados

**Após atualizar no Render, o botão "Gerar 60 Questões" funcionará perfeitamente!**