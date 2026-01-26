# 📖 Instruções Completas - Do Zero ao Online

## 🎯 Objetivo

Hospedar o Sistema de Simulados IBGP no GitHub e deixá-lo acessível online gratuitamente.

---

## 📋 Pré-requisitos

- [ ] Git instalado (https://git-scm.com/downloads)
- [ ] Conta no GitHub (https://github.com/signup)
- [ ] Conta em plataforma de deploy (Render.com recomendado)

---

## 🚀 PARTE 1: Hospedar no GitHub

### Método A: Script Automático (Recomendado)

#### Windows:
1. Abra PowerShell ou CMD na pasta do projeto
2. Execute:
   ```bash
   setup_github.bat
   ```
3. Siga as instruções na tela
4. Pronto! ✅

#### Linux/Mac:
1. Abra Terminal na pasta do projeto
2. Execute:
   ```bash
   bash setup_github.sh
   ```
3. Siga as instruções na tela
4. Pronto! ✅

### Método B: Manual

#### Passo 1: Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. Preencha:
   - **Repository name**: `simulados-ibgp`
   - **Description**: `Sistema de Simulados Adaptativos - Técnico em Informática`
   - **Public**: ✅ (para ser acessível)
   - **Initialize**: ❌ NÃO marque nada
3. Clique "Create repository"
4. **Copie a URL**: `https://github.com/SEU-USUARIO/simulados-ibgp.git`

#### Passo 2: Configurar Git Local

Abra terminal/CMD na pasta do projeto:

```bash
# Inicializar Git
git init

# Configurar usuário (se necessário)
git config user.name "Seu Nome"
git config user.email "seu@email.com"

# Adicionar todos os arquivos
git add .

# Criar commit
git commit -m "Initial commit: Sistema completo de simulados IBGP"

# Criar branch main
git branch -M main

# Conectar com GitHub (substitua SEU-USUARIO)
git remote add origin https://github.com/SEU-USUARIO/simulados-ibgp.git

# Enviar para GitHub
git push -u origin main
```

#### Passo 3: Verificar

1. Acesse: `https://github.com/SEU-USUARIO/simulados-ibgp`
2. Verifique se todos os arquivos estão lá
3. O README.md deve aparecer na página inicial

✅ **Código agora está no GitHub!**

---

## 🌐 PARTE 2: Deploy Online (Render.com)

### Por que Render.com?
- ✅ Gratuito
- ✅ Fácil de usar
- ✅ Suporta Docker
- ✅ PostgreSQL incluído
- ✅ Deploy automático

### Passo 1: Criar Conta

1. Acesse: https://render.com
2. Clique "Get Started"
3. Faça login com GitHub
4. Autorize acesso ao Render

### Passo 2: Deploy do Backend (API)

1. No dashboard do Render, clique **"New +"**
2. Selecione **"Web Service"**
3. Clique **"Connect a repository"**
4. Encontre e selecione **"simulados-ibgp"**
5. Clique **"Connect"**

6. Configure:
   - **Name**: `simulados-api`
   - **Region**: Escolha mais próximo (ex: Oregon)
   - **Branch**: `main`
   - **Root Directory**: deixe vazio
   - **Environment**: `Docker`
   - **Dockerfile Path**: `docker/Dockerfile.api`
   - **Docker Build Context Directory**: `api`
   - **Instance Type**: `Free`

7. **NÃO clique em "Create" ainda!** Vamos adicionar variáveis primeiro.

8. Role até **"Environment Variables"** e adicione:

   ```
   POSTGRES_HOST=<vamos-preencher-depois>
   POSTGRES_PORT=5432
   POSTGRES_DB=simulados_db
   POSTGRES_USER=simulados_user
   POSTGRES_PASSWORD=SuaSenhaSegura123!
   SECRET_KEY=sua-chave-secreta-aleatoria-aqui-123456
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REDIS_HOST=<vamos-preencher-depois>
   REDIS_PORT=6379
   ENVIRONMENT=production
   DEBUG=false
   ```

9. Agora clique **"Create Web Service"**

10. Aguarde o build (5-10 minutos)

### Passo 3: Criar PostgreSQL

1. No dashboard, clique **"New +"**
2. Selecione **"PostgreSQL"**
3. Configure:
   - **Name**: `simulados-db`
   - **Database**: `simulados_db`
   - **User**: `simulados_user`
   - **Region**: Mesma do web service
   - **PostgreSQL Version**: 15
   - **Plan**: `Free`

4. Clique **"Create Database"**

5. Aguarde criação (2-3 minutos)

6. Quando pronto, clique no banco criado

7. Na aba **"Info"**, copie:
   - **Internal Database URL** (começa com `postgres://`)
   - **Hostname** (ex: `dpg-xxxxx-a`)

### Passo 4: Criar Redis

1. No dashboard, clique **"New +"**
2. Selecione **"Redis"**
3. Configure:
   - **Name**: `simulados-redis`
   - **Region**: Mesma dos outros
   - **Plan**: `Free`

4. Clique **"Create Redis"**

5. Quando pronto, copie o **Hostname**

### Passo 5: Atualizar Variáveis do Backend

1. Volte para **simulados-api**
2. Vá em **"Environment"** (menu lateral)
3. Atualize:
   - `POSTGRES_HOST`: Cole o hostname do PostgreSQL
   - `REDIS_HOST`: Cole o hostname do Redis

4. Clique **"Save Changes"**

5. O serviço vai fazer redeploy automaticamente

### Passo 6: Deploy do Frontend

1. No dashboard, clique **"New +"**
2. Selecione **"Static Site"**
3. Conecte o mesmo repositório **"simulados-ibgp"**

4. Configure:
   - **Name**: `simulados-web`
   - **Branch**: `main`
   - **Root Directory**: `web`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

5. Adicione variável de ambiente:
   ```
   VITE_API_URL=https://simulados-api.onrender.com
   ```
   (Substitua pela URL real do seu backend)

6. Clique **"Create Static Site"**

7. Aguarde build (3-5 minutos)

### Passo 7: Popular Banco de Dados

1. Vá para **simulados-api**
2. Clique em **"Shell"** (menu lateral)
3. Execute:
   ```bash
   python scripts/seed_database.py
   ```

4. Aguarde mensagem de sucesso

### Passo 8: Testar Sistema

1. Copie a URL do frontend (ex: `https://simulados-web.onrender.com`)
2. Acesse no navegador
3. Faça login:
   - Username: `teste`
   - Password: `senha123`

4. Teste:
   - Upload de edital
   - Geração de questões
   - Criação de simulado
   - Execução de simulado

✅ **Sistema online e funcionando!**

---

## 📝 PARTE 3: Atualizar README

Edite o `README.md` e adicione no topo:

```markdown
## 🌐 Demo Online

**Acesse o sistema**: https://simulados-web.onrender.com

**API Docs**: https://simulados-api.onrender.com/docs

### Credenciais de Teste
- Username: `teste`
- Password: `senha123`
```

Faça commit e push:

```bash
git add README.md
git commit -m "Add: Link da demo online"
git push origin main
```

---

## 🎉 PARTE 4: Compartilhar

### Seu sistema está online!

**URLs**:
- Frontend: `https://simulados-web.onrender.com`
- API: `https://simulados-api.onrender.com`
- Swagger: `https://simulados-api.onrender.com/docs`
- GitHub: `https://github.com/SEU-USUARIO/simulados-ibgp`

### Compartilhe em:

1. **LinkedIn**:
   ```
   🚀 Acabei de lançar um Sistema de Simulados Adaptativos para concursos públicos!
   
   ✅ Ingestão automática de editais
   ✅ Geração de questões no estilo IBGP
   ✅ Treino adaptativo com algoritmo SRS
   ✅ Analytics completo
   
   Acesse: https://simulados-web.onrender.com
   Código: https://github.com/SEU-USUARIO/simulados-ibgp
   
   #desenvolvedor #concursos #opensource
   ```

2. **Twitter**:
   ```
   🎯 Sistema de Simulados para concursos públicos
   
   ✅ Open source
   ✅ Treino adaptativo
   ✅ Gratuito
   
   Demo: https://simulados-web.onrender.com
   GitHub: https://github.com/SEU-USUARIO/simulados-ibgp
   
   #coding #opensource
   ```

3. **GitHub README**: Já atualizado ✅

4. **Portfólio**: Adicione como projeto destaque

5. **Grupos de Concursos**: Compartilhe o link

---

## 🔧 Manutenção

### Ver Logs

1. Acesse Render dashboard
2. Clique no serviço (api ou web)
3. Vá em "Logs"

### Fazer Backup

1. Vá em **simulados-db**
2. Clique em **"Backups"**
3. Clique **"Create Backup"**

### Atualizar Sistema

```bash
# Fazer mudanças localmente
git add .
git commit -m "Update: descrição"
git push origin main

# Render faz redeploy automático!
```

---

## 📊 Monitoramento

### Render Dashboard

- **Status**: Verde = OK
- **Logs**: Ver erros em tempo real
- **Metrics**: CPU, RAM, requests

### Uptime

Render Free tier:
- Pode dormir após 15 min de inatividade
- Acorda automaticamente ao acessar
- Primeiro acesso pode demorar ~30s

Para manter sempre ativo (opcional):
- Use serviço de ping (ex: UptimeRobot)
- Ou upgrade para plano pago

---

## 🆘 Problemas Comuns

### Build Failed

**Solução**:
1. Veja logs no Render
2. Verifique Dockerfile paths
3. Confirme variáveis de ambiente

### Cannot Connect to Database

**Solução**:
1. Verifique POSTGRES_HOST
2. Confirme que PostgreSQL está "Available"
3. Teste conexão no Shell

### Frontend não carrega

**Solução**:
1. Verifique VITE_API_URL
2. Confirme CORS no backend
3. Rebuild do frontend

### 502 Bad Gateway

**Solução**:
1. Backend pode estar dormindo (aguarde 30s)
2. Verifique logs do backend
3. Confirme que backend está "Available"

---

## 📚 Recursos Adicionais

- **Guia Completo**: [GITHUB_SETUP.md](GITHUB_SETUP.md)
- **Deploy Rápido**: [DEPLOY_RAPIDO.md](DEPLOY_RAPIDO.md)
- **FAQ**: [docs/FAQ.md](docs/FAQ.md)
- **Deployment**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## ✅ Checklist Final

- [ ] Código no GitHub
- [ ] Backend deployado no Render
- [ ] PostgreSQL criado e conectado
- [ ] Redis criado e conectado
- [ ] Frontend deployado
- [ ] Banco populado com seed
- [ ] Sistema testado online
- [ ] README atualizado com links
- [ ] Compartilhado nas redes sociais
- [ ] Adicionado ao portfólio

---

## 🎯 Resultado Final

✅ **Sistema 100% funcional e online**
✅ **Acessível 24/7 gratuitamente**
✅ **URL pública para compartilhar**
✅ **Código open source no GitHub**
✅ **Pronto para receber contribuições**

---

**Parabéns! 🎉**

Você agora tem um sistema completo de simulados online, acessível para qualquer pessoa, hospedado gratuitamente!

**Tempo total**: ~30 minutos
**Custo**: R$ 0,00
**Resultado**: Sistema profissional online!

---

**Dúvidas?** Abra uma issue no GitHub ou consulte a documentação completa.
