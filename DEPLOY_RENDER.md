# 🚀 Deploy no Render - Sistema Porto Velho

**Tempo estimado:** 15 minutos  
**Custo:** GRATUITO

---

## 📋 PRÉ-REQUISITOS

✅ Repositório GitHub: https://github.com/Dev-HP/simulados-ibgp  
✅ Conta no Render: https://render.com (criar se não tiver)  
✅ API Key do Gemini: Configure no Render (não exponha no código!)

---

## 🎯 PASSO 1: Preparar Código (2 minutos)

### 1.1 Atualizar Repositório

```bash
cd "C:\sistema camara"
git add .
git commit -m "Preparar para deploy no Render"
git push origin main
```

---

## 🎯 PASSO 2: Deploy da API (5 minutos)

### 2.1 Criar Web Service

1. **Acessar Render:**
   - Ir para: https://dashboard.render.com
   - Clicar em **"New +"** → **"Web Service"**

2. **Conectar Repositório:**
   - Clicar em **"Connect account"** (se primeira vez)
   - Autorizar acesso ao GitHub
   - Selecionar: **`Dev-HP/simulados-ibgp`**
   - Clicar em **"Connect"**

3. **Configurar Serviço:**
   ```
   Name: simulados-api-porto-velho
   Region: Oregon (US West) - mais próximo
   Branch: main
   Root Directory: api
   Environment: Docker
   Instance Type: Free
   ```

4. **Adicionar Variáveis de Ambiente:**
   
   Clicar em **"Advanced"** → **"Add Environment Variable"**
   
   Adicionar estas variáveis:
   
   ```
   GEMINI_API_KEY=[SUA_CHAVE_AQUI]
   DATABASE_URL=sqlite:///./simulados.db
   SECRET_KEY=render-secret-key-2026-porto-velho-concurso
   ENVIRONMENT=production
   ```

5. **Criar Serviço:**
   - Clicar em **"Create Web Service"**
   - Aguardar build (~3-5 minutos)
   - URL gerada: `https://simulados-api-porto-velho.onrender.com`

---

## 🎯 PASSO 3: Deploy do Frontend (5 minutos)

### 3.1 Criar Static Site

1. **Novo Serviço:**
   - Clicar em **"New +"** → **"Static Site"**

2. **Conectar Repositório:**
   - Selecionar: **`Dev-HP/simulados-ibgp`**
   - Clicar em **"Connect"**

3. **Configurar Build:**
   ```
   Name: simulados-web-porto-velho
   Branch: main
   Root Directory: web
   Build Command: npm install && npm run build
   Publish Directory: web/dist
   ```

4. **Adicionar Variável de Ambiente:**
   
   Clicar em **"Advanced"** → **"Add Environment Variable"**
   
   ```
   VITE_API_URL=https://simulados-api-porto-velho.onrender.com
   ```
   
   **IMPORTANTE:** Substitua pela URL real da sua API (do Passo 2)

5. **Criar Site:**
   - Clicar em **"Create Static Site"**
   - Aguardar build (~3-5 minutos)
   - URL gerada: `https://simulados-web-porto-velho.onrender.com`

---

## 🎯 PASSO 4: Configurar CORS (2 minutos)

### 4.1 Atualizar API para aceitar Frontend

Editar `api/main.py` e adicionar a URL do frontend no CORS:

```python
# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://simulados-web-porto-velho.onrender.com"  # Adicionar esta linha
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Fazer commit e push:

```bash
git add api/main.py
git commit -m "Adicionar URL do Render no CORS"
git push origin main
```

O Render vai fazer redeploy automático da API.

---

## 🎯 PASSO 5: Popular Banco de Dados (3 minutos)

### 5.1 Criar Tópicos

1. **Acessar Shell da API:**
   - Dashboard Render → `simulados-api-porto-velho`
   - Clicar em **"Shell"** (no menu lateral)

2. **Executar Script:**
   ```bash
   python criar_topicos.py
   ```
   
   Deve criar os 54 tópicos focados em Porto Velho.

### 5.2 Criar Usuário de Teste

No mesmo shell:

```bash
python -c "
from database import SessionLocal
from models import User
from passlib.context import CryptContext

db = SessionLocal()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

user = User(
    username='teste',
    email='teste@portovelho.com',
    hashed_password=pwd_context.hash('teste123'),
    full_name='Usuário Teste'
)

db.add(user)
db.commit()
print('Usuário criado!')
"
```

---

## 🎯 PASSO 6: Testar Sistema (2 minutos)

### 6.1 Acessar Frontend

Abrir no navegador:
```
https://simulados-web-porto-velho.onrender.com
```

### 6.2 Fazer Login

```
Usuário: teste
Senha: teste123
```

### 6.3 Testar Funcionalidades

1. ✅ Dashboard carrega
2. ✅ Ver tópicos (54 tópicos)
3. ✅ Gerar questão com IA
4. ✅ Fazer prova completa

---

## 🎉 PRONTO! SISTEMA ONLINE

### 🌐 Suas URLs:

**Frontend (Interface):**
```
https://simulados-web-porto-velho.onrender.com
```

**API (Backend):**
```
https://simulados-api-porto-velho.onrender.com
```

**Documentação da API:**
```
https://simulados-api-porto-velho.onrender.com/docs
```

---

## 📊 MONITORAMENTO

### Ver Logs

**API:**
- Dashboard → `simulados-api-porto-velho` → **"Logs"**

**Frontend:**
- Dashboard → `simulados-web-porto-velho` → **"Logs"**

### Métricas

- Dashboard → Serviço → **"Metrics"**
- Ver uso de CPU, memória, requests

---

## ⚠️ LIMITAÇÕES DO PLANO FREE

### API (Web Service Free):
- ✅ 750 horas/mês (suficiente)
- ⚠️ Dorme após 15 min inativo
- ⚠️ Primeiro acesso demora ~30s (wake up)
- ✅ 512 MB RAM
- ✅ 0.1 CPU

### Frontend (Static Site):
- ✅ 100 GB bandwidth/mês
- ✅ Sempre ativo (não dorme)
- ✅ CDN global

### Banco de Dados:
- ✅ SQLite (arquivo local)
- ⚠️ Dados resetam a cada deploy
- 💡 Para produção: usar PostgreSQL pago ($7/mês)

---

## 💡 DICAS IMPORTANTES

### 1. Manter API Ativa

A API dorme após 15 min. Para manter ativa:

**Opção A: Ping automático (UptimeRobot)**
1. Criar conta: https://uptimerobot.com
2. Add Monitor → HTTP(s)
3. URL: `https://simulados-api-porto-velho.onrender.com/api/health`
4. Interval: 5 minutos

**Opção B: Cron Job (cron-job.org)**
1. Criar conta: https://cron-job.org
2. Create cronjob
3. URL: sua API
4. Interval: */5 * * * * (a cada 5 min)

### 2. Backup do Banco

Como SQLite reseta, faça backup regular:

```bash
# No shell do Render
python -c "
from database import SessionLocal
from models import Question, Topic
import json

db = SessionLocal()
questions = db.query(Question).all()
topics = db.query(Topic).all()

backup = {
    'questions': [q.__dict__ for q in questions],
    'topics': [t.__dict__ for t in topics]
}

with open('backup.json', 'w') as f:
    json.dump(backup, f)

print('Backup criado!')
"
```

### 3. Gerar Questões

Use a interface web para gerar questões:
- 10-15 por vez
- Aguardar 1 minuto entre gerações
- Focar em Informática primeiro

---

## 🔧 TROUBLESHOOTING

### API não responde

1. Ver logs no Dashboard
2. Verificar variáveis de ambiente
3. Testar endpoint: `/api/health`

### Frontend não carrega

1. Verificar `VITE_API_URL` está correto
2. Ver logs do build
3. Testar API diretamente

### CORS Error

1. Verificar URL do frontend no `api/main.py`
2. Fazer commit e push
3. Aguardar redeploy

### Gemini não funciona

1. Verificar `GEMINI_API_KEY` no Dashboard
2. Testar API key: https://aistudio.google.com
3. Ver logs da API

---

## 📱 COMPARTILHAR

### Adicionar ao README

```markdown
## 🌐 Demo Online

**Acesse o sistema:** https://simulados-web-porto-velho.onrender.com

**Credenciais de teste:**
- Usuário: `teste`
- Senha: `teste123`

**Foco:** Concurso Técnico em Informática - Câmara de Porto Velho/RO
```

### Divulgar

- ✅ LinkedIn
- ✅ Grupos de concursos
- ✅ Comunidades de dev
- ✅ Portfólio pessoal

---

## 🎯 PRÓXIMOS PASSOS

1. ✅ Sistema online
2. ⏭️ Gerar 200-400 questões
3. ⏭️ Testar provas completas
4. ⏭️ Compartilhar com colegas
5. ⏭️ Estudar para o concurso!

---

## 📞 SUPORTE

**Problemas?**
- Ver logs no Dashboard
- Ler documentação: https://render.com/docs
- Abrir issue no GitHub

**Dúvidas sobre o sistema?**
- Ler: `LEIA_PRIMEIRO.md`
- Ler: `GUIA_COMPLETO_CONCURSO.md`

---

## ✅ CHECKLIST FINAL

- [ ] API deployada no Render
- [ ] Frontend deployado no Render
- [ ] CORS configurado
- [ ] Tópicos criados (54)
- [ ] Usuário teste criado
- [ ] Sistema testado
- [ ] URLs funcionando
- [ ] README atualizado
- [ ] Sistema compartilhado

---

**Boa sorte no concurso! 🚀📚**

**Sistema online em:** https://simulados-web-porto-velho.onrender.com
