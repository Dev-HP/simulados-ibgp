# 🚨 EMERGÊNCIA: API KEY COMPROMETIDA

## PROBLEMA
- Google detectou API key vazada
- Bloqueou a key por segurança (403 Forbidden)
- Sistema não consegue gerar questões

## SOLUÇÃO IMEDIATA (5 MINUTOS)

### 1. Gerar Nova API Key
1. Acesse: https://console.cloud.google.com/apis/credentials
2. Clique em "Create Credentials" → "API Key"
3. Copie a nova key
4. **NÃO COMPARTILHE EM LUGAR NENHUM!**

### 2. Atualizar no Render
1. Acesse: https://dashboard.render.com
2. Vá em "simulados-ibgp" (API service)
3. Settings → Environment
4. Encontre: GEMINI_API_KEY
5. Clique "Edit"
6. Cole a NOVA key
7. Clique "Save Changes"

### 3. Aguardar Redeploy
- Render fará redeploy automático (2-3 min)
- Sistema voltará a funcionar

## CAUSA DO VAZAMENTO
A API key foi exposta em commits do GitHub, mesmo após remoção.
O GitHub Scanner detectou e reportou para a Google.

## PREVENÇÃO
✅ Nunca commitar API keys
✅ Usar apenas variáveis de ambiente
✅ Verificar .gitignore

## STATUS ATUAL
❌ Geração de questões: BLOQUEADA
✅ Login/navegação: FUNCIONANDO
✅ Questões existentes: FUNCIONANDO

Após atualizar a key, tudo voltará ao normal!