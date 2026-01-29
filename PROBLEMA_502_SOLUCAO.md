# 🚨 PROBLEMA: API Retornando 502 Bad Gateway

**Data:** 29/01/2026  
**Status:** ❌ API OFFLINE  
**Impacto:** Sistema não funciona

---

## 🔍 DIAGNÓSTICO

### Erros Identificados:

1. **502 Bad Gateway**
   ```
   GET https://simulados-ibgp.onrender.com/api/*
   Status: 502 (Bad Gateway)
   ```
   - API não está respondendo
   - Serviço pode estar crashando
   - Ou ainda em deploy

2. **CORS Error** (secundário)
   ```
   Access to XMLHttpRequest blocked by CORS policy
   ```
   - Aparece porque API está offline
   - CORS está configurado corretamente no código
   - Não é o problema principal

### Verificação Realizada:
```bash
python verificar_deploy_rapido.py
```

**Resultado:**
- ❌ API: 502 Bad Gateway
- ✅ Frontend: ONLINE
- ⚠️ Endpoint novo: Não verificável (API offline)

---

## 🎯 CAUSAS POSSÍVEIS

### 1. Deploy Ainda em Andamento
- Render pode demorar 10-15 minutos
- Último push foi há ~10 minutos
- **Probabilidade:** 70%

### 2. Erro no Build/Deploy
- Código com erro de sintaxe
- Dependência faltando
- Variável de ambiente não configurada
- **Probabilidade:** 20%

### 3. Crash na Inicialização
- Erro ao conectar no banco
- Erro ao importar módulos
- Erro em algum router
- **Probabilidade:** 10%

---

## 🛠️ SOLUÇÕES

### Solução 1: AGUARDAR (Recomendado)

**Se deploy ainda está em andamento:**

```bash
# Aguarde 5-10 minutos e verifique novamente
python verificar_deploy_rapido.py
```

**Ou acesse diretamente:**
```
https://simulados-ibgp.onrender.com/health
```

Se retornar `{"status": "healthy"}`, API está OK!

---

### Solução 2: VERIFICAR LOGS NO RENDER

**Passo a passo:**

1. Acesse: https://dashboard.render.com
2. Faça login
3. Selecione serviço: `simulados-ibgp`
4. Clique em "Logs"
5. Veja os erros

**Erros comuns:**
- `ModuleNotFoundError` → Dependência faltando
- `Connection refused` → Banco não conecta
- `Port already in use` → Problema de porta
- `SyntaxError` → Erro de código

---

### Solução 3: VERIFICAR VARIÁVEIS DE AMBIENTE

**No Render Dashboard:**

1. Serviço → Settings → Environment
2. Verificar se existe:
   - `GEMINI_API_KEY` = AIzaSyAJdlxhkUPf2ykYpd_7teyP4ge9zukGe6s
   - `DATABASE_URL` = (gerado automaticamente)
   - `SECRET_KEY` = (qualquer string)

**Se faltando, adicionar e fazer redeploy:**
```
Settings → Environment → Add Environment Variable
```

---

### Solução 4: FORÇAR REDEPLOY

**Se deploy travou:**

1. Render Dashboard
2. Serviço `simulados-ibgp`
3. Botão "Manual Deploy"
4. Selecionar branch `main`
5. Deploy

---

### Solução 5: ROLLBACK (Último Recurso)

**Se novo código tem erro:**

1. Render Dashboard
2. Serviço → Deploys
3. Encontrar deploy anterior que funcionava
4. Clicar "Redeploy"

**Ou via Git:**
```bash
# Reverter último commit
git revert HEAD

# Push
git push origin main
```

---

## 🔍 VERIFICAÇÕES ADICIONAIS

### 1. Testar Health Check Direto
```bash
curl https://simulados-ibgp.onrender.com/health
```

**Esperado:**
```json
{"status": "healthy"}
```

**Se retornar 502:**
- API está crashando
- Ver logs no Render

### 2. Testar API Health
```bash
curl https://simulados-ibgp.onrender.com/api/health
```

**Esperado:**
```json
{"status": "healthy"}
```

### 3. Verificar Frontend
```bash
curl https://simulados-ibgp-1.onrender.com
```

**Esperado:**
- HTML da página
- Status 200

---

## 📊 TIMELINE ESPERADO

### Deploy Normal:
```
0 min  → Push para GitHub
1 min  → GitHub Actions inicia
2 min  → Render detecta push
3 min  → Build inicia
5 min  → Build completa
7 min  → Deploy inicia
10 min → API online
12 min → Tudo funcionando
```

### Se Passou de 15 Minutos:
- ❌ Algo está errado
- Ver logs no Render
- Verificar erros

---

## 🎯 AÇÃO IMEDIATA

### AGORA (Faça isso):

1. **Aguarde 5 minutos**
   ```
   Último push foi há ~10 minutos
   Deploy pode estar finalizando
   ```

2. **Verifique novamente:**
   ```bash
   python verificar_deploy_rapido.py
   ```

3. **Se ainda 502:**
   - Acesse Render Dashboard
   - Veja os logs
   - Identifique o erro

4. **Se logs mostram erro:**
   - Copie o erro
   - Cole aqui para análise
   - Vamos corrigir

---

## 💡 DICAS

### Enquanto API está offline:

1. **Não tente usar o sistema**
   - Vai dar erro
   - Aguarde API voltar

2. **Não faça novos commits**
   - Pode piorar
   - Aguarde deploy atual

3. **Monitore os logs**
   - Render Dashboard → Logs
   - Veja o que está acontecendo

4. **Seja paciente**
   - Deploy pode demorar
   - Render free tier é lento

---

## 🚀 QUANDO API VOLTAR

### Verificar:
```bash
# 1. Health check
curl https://simulados-ibgp.onrender.com/health

# 2. Teste completo
python testar_producao_completo.py

# 3. Acessar sistema
https://simulados-ibgp-1.onrender.com/ai-generator
```

### Usar:
1. Login: `teste` / `teste123`
2. Clicar: "🚀 GERAR TODAS AS 60 QUESTÕES"
3. Aguardar: 15-20 minutos
4. Estudar!

---

## 📞 PRÓXIMOS PASSOS

### Opção A: Aguardar (Recomendado)
```
1. Aguarde 5-10 minutos
2. Execute: python verificar_deploy_rapido.py
3. Se OK, use o sistema
4. Se 502, vá para Opção B
```

### Opção B: Verificar Logs
```
1. Acesse: https://dashboard.render.com
2. Serviço: simulados-ibgp
3. Logs: Veja os erros
4. Copie e cole aqui
```

### Opção C: Forçar Redeploy
```
1. Render Dashboard
2. Manual Deploy
3. Branch: main
4. Aguarde 10-15 minutos
```

---

## ✅ CHECKLIST

Antes de pedir ajuda:

- [ ] Aguardei pelo menos 10 minutos após último push
- [ ] Executei `python verificar_deploy_rapido.py`
- [ ] Testei `curl https://simulados-ibgp.onrender.com/health`
- [ ] Verifiquei logs no Render Dashboard
- [ ] Verifiquei variáveis de ambiente no Render
- [ ] Tentei forçar redeploy manual

---

## 🎯 CONCLUSÃO

**Problema:** API retornando 502 Bad Gateway  
**Causa Provável:** Deploy ainda em andamento  
**Solução:** Aguardar 5-10 minutos e verificar novamente  

**Se persistir:** Ver logs no Render e identificar erro específico

---

**Última atualização:** 29/01/2026  
**Status:** 🔍 INVESTIGANDO  
**Próxima ação:** AGUARDAR E VERIFICAR LOGS

