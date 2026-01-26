# 🚀 Guia Completo: Hospedar no GitHub e Deploy Online

## Parte 1: Subir para o GitHub

### Passo 1: Criar Repositório no GitHub

1. Acesse https://github.com/new
2. Preencha:
   - **Repository name**: `simulados-ibgp`
   - **Description**: `Sistema de Simulados Adaptativos - Técnico em Informática (IBGP)`
   - **Visibility**: Public (para ser acessível)
   - ❌ **NÃO** marque "Initialize with README" (já temos)
3. Clique em "Create repository"

### Passo 2: Inicializar Git Local

Abra o terminal na pasta do projeto e execute:

```bash
# Inicializar repositório
git init

# Adicionar todos os arquivos
git add .

# Primeiro commit
git commit -m "Initial commit: Sistema completo de simulados IBGP"

# Adicionar remote (substitua SEU-USUARIO pelo seu username do GitHub)
git remote add origin https://github.com/SEU-USUARIO/simulados-ibgp.git

# Criar branch main
git branch -M main

# Push para GitHub
git push -u origin main
```

### Passo 3: Verificar Upload

1. Acesse: `https://github.com/SEU-USUARIO/simulados-ibgp`
2. Verifique se todos os arquivos estão lá
3. O README.md deve aparecer automaticamente na página inicial

---

## Parte 2: Deploy Online (Opções Gratuitas)

### 🎯 Opção 1: Render.com (RECOMENDADO - Mais Fácil)

**Vantagens**: Gratuito, fácil, suporta Docker, PostgreSQL incluído

#### 2.1. Criar Conta
1. Acesse https://render.com
2. Clique em "Get Started"
3. Faça login com GitHub

#### 2.2. Deploy do Backend (API)

1. No dashboard, clique em "New +"
2. Selecione "Web Service"
3. Conecte seu repositório GitHub
4. Configure:
   - **Name**: `simulados-api`
   - **Environment**: `Docker`
   - **Dockerfile Path**: `docker/Dockerfile.api`
   - **Instance Type**: `Free`
   
5. Adicione variáveis de ambiente:
   ```
   POSTGRES_HOST=<render-postgres-host>
   POSTGRES_PORT=5432
   POSTGRES_DB=simulados_db
   POSTGRES_USER=simulados_user
   POSTGRES_PASSWORD=<senha-segura>
   SECRET_KEY=<gerar-chave-aleatoria>
   REDIS_HOST=<render-redis-host>
   ENVIRONMENT=production
   DEBUG=false
   ```

6. Clique em "Create Web Service"

#### 2.3. Criar PostgreSQL

1. No dashboard, clique em "New +"
2. Selecione "PostgreSQL"
3. Configure:
   - **Name**: `simulados-db`
   - **Database**: `simulados_db`
   - **User**: `simulados_user`
   - **Region**: Mesma do web service
   - **Plan**: `Free`

4. Clique em "Create Database"
5. Copie a "Internal Database URL"
6. Volte no Web Service e atualize as variáveis de ambiente

#### 2.4. Deploy do Frontend (Web)

1. No dashboard, clique em "New +"
2. Selecione "Static Site"
3. Conecte seu repositório
4. Configure:
   - **Name**: `simulados-web`
   - **Build Command**: `cd web && npm install && npm run build`
   - **Publish Directory**: `web/dist`

5. Adicione variável de ambiente:
   ```
   VITE_API_URL=https://simulados-api.onrender.com
   ```

6. Clique em "Create Static Site"

#### 2.5. Acessar Sistema

Após deploy (5-10 minutos):
- **Frontend**: `https://simulados-web.onrender.com`
- **API**: `https://simulados-api.onrender.com`
- **Swagger**: `https://simulados-api.onrender.com/docs`

---

### 🎯 Opção 2: Railway.app (Alternativa Fácil)

**Vantagens**: Gratuito, muito simples, suporta Docker

#### 2.1. Criar Conta
1. Acesse https://railway.app
2. Clique em "Start a New Project"
3. Faça login com GitHub

#### 2.2. Deploy Completo

1. Clique em "Deploy from GitHub repo"
2. Selecione `simulados-ibgp`
3. Railway detectará automaticamente o docker-compose.yml
4. Clique em "Deploy"

#### 2.3. Configurar Variáveis

1. Clique em cada serviço (api, web, postgres, redis)
2. Vá em "Variables"
3. Adicione as variáveis do `.env.example`

#### 2.4. Acessar

Railway gerará URLs automaticamente:
- Frontend: `https://simulados-web.up.railway.app`
- API: `https://simulados-api.up.railway.app`

---

### 🎯 Opção 3: Fly.io (Para Usuários Avançados)

**Vantagens**: Gratuito, rápido, global

#### 3.1. Instalar CLI

```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

#### 3.2. Login e Deploy

```bash
# Login
fly auth login

# Deploy API
cd api
fly launch --name simulados-api --region gru

# Deploy Web
cd ../web
fly launch --name simulados-web --region gru
```

#### 3.3. Criar PostgreSQL

```bash
fly postgres create --name simulados-db --region gru
fly postgres attach simulados-db -a simulados-api
```

---

### 🎯 Opção 4: Heroku (Clássico)

**Vantagens**: Conhecido, estável

#### 4.1. Criar Conta
1. Acesse https://heroku.com
2. Crie conta gratuita

#### 4.2. Instalar CLI

```bash
# Windows
# Baixe de: https://devcenter.heroku.com/articles/heroku-cli

# Mac
brew tap heroku/brew && brew install heroku
```

#### 4.3. Deploy

```bash
# Login
heroku login

# Criar apps
heroku create simulados-api
heroku create simulados-web

# Adicionar PostgreSQL
heroku addons:create heroku-postgresql:mini -a simulados-api

# Adicionar Redis
heroku addons:create heroku-redis:mini -a simulados-api

# Deploy API
git subtree push --prefix api heroku main

# Deploy Web
git subtree push --prefix web heroku main
```

---

## Parte 3: Configuração Pós-Deploy

### 3.1. Popular Banco de Dados

Após deploy, execute o seed:

```bash
# Render.com
# Vá no dashboard > Shell > Execute:
python scripts/seed_database.py

# Railway
railway run python scripts/seed_database.py

# Fly.io
fly ssh console -a simulados-api
python scripts/seed_database.py

# Heroku
heroku run python scripts/seed_database.py -a simulados-api
```

### 3.2. Testar Sistema

1. Acesse o frontend
2. Faça login com: `teste` / `senha123`
3. Faça upload do edital
4. Gere banco de questões
5. Crie e execute simulado

### 3.3. Configurar Domínio Customizado (Opcional)

#### Render.com
1. Vá em Settings > Custom Domain
2. Adicione seu domínio
3. Configure DNS conforme instruções

#### Railway
1. Vá em Settings > Domains
2. Adicione domínio customizado
3. Configure CNAME no seu DNS

---

## Parte 4: Manutenção e Monitoramento

### 4.1. Ver Logs

```bash
# Render.com
# Dashboard > Logs

# Railway
railway logs

# Fly.io
fly logs -a simulados-api

# Heroku
heroku logs --tail -a simulados-api
```

### 4.2. Backup do Banco

```bash
# Render.com
# Dashboard > Database > Backups

# Railway
# Automático

# Fly.io
fly postgres backup create -a simulados-db

# Heroku
heroku pg:backups:capture -a simulados-api
```

### 4.3. Atualizar Sistema

```bash
# Fazer mudanças localmente
git add .
git commit -m "Update: descrição"
git push origin main

# Deploy automático via GitHub Actions
# Ou manualmente:
# Render/Railway: Redeploy automático
# Fly.io: fly deploy
# Heroku: git push heroku main
```

---

## Parte 5: Compartilhar com o Mundo

### 5.1. Atualizar README com Links

Edite o README.md:

```markdown
## 🌐 Demo Online

- **Frontend**: https://simulados-web.onrender.com
- **API**: https://simulados-api.onrender.com/docs
- **Repositório**: https://github.com/SEU-USUARIO/simulados-ibgp

### Credenciais de Teste
- Username: `teste`
- Password: `senha123`
```

### 5.2. Adicionar Badges

No README.md, adicione:

```markdown
[![Deploy](https://img.shields.io/badge/deploy-online-success)](https://simulados-web.onrender.com)
[![API](https://img.shields.io/badge/API-docs-blue)](https://simulados-api.onrender.com/docs)
[![GitHub](https://img.shields.io/github/stars/SEU-USUARIO/simulados-ibgp?style=social)](https://github.com/SEU-USUARIO/simulados-ibgp)
```

### 5.3. Criar Release

```bash
git tag -a v1.0.0 -m "Release 1.0.0: Sistema completo"
git push origin v1.0.0
```

No GitHub:
1. Vá em "Releases"
2. Clique em "Create a new release"
3. Selecione tag v1.0.0
4. Adicione descrição
5. Publique

---

## 🎉 Pronto! Sistema Online

Seu sistema estará acessível em:
- **URL Pública**: `https://seu-app.onrender.com`
- **Sempre disponível**: 24/7
- **Gratuito**: Sem custos
- **Escalável**: Pode crescer conforme necessidade

### Compartilhe:
- LinkedIn
- Twitter
- Grupos de concursos
- Fóruns de TI
- Comunidades de desenvolvedores

---

## 📊 Monitoramento de Uso

### Analytics (Opcional)

Adicione Google Analytics:

1. Crie conta em https://analytics.google.com
2. Obtenha ID de rastreamento
3. Adicione no `web/index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

---

## 🆘 Troubleshooting

### Erro de Build
- Verifique logs no dashboard
- Confirme Dockerfile paths
- Verifique variáveis de ambiente

### Erro de Conexão com Banco
- Verifique DATABASE_URL
- Confirme que PostgreSQL está rodando
- Teste conexão manualmente

### Frontend não carrega
- Verifique VITE_API_URL
- Confirme CORS no backend
- Verifique build do Vite

### Performance lenta
- Upgrade para plano pago
- Otimize queries do banco
- Adicione cache Redis
- Use CDN para assets

---

## 💡 Dicas Finais

1. **Mantenha atualizado**: Push regular para GitHub
2. **Monitore logs**: Verifique erros diariamente
3. **Backup**: Configure backups automáticos
4. **Segurança**: Use senhas fortes, atualize dependências
5. **Documentação**: Mantenha README atualizado
6. **Comunidade**: Responda issues, aceite PRs

---

## 🎯 Próximos Passos

1. [ ] Subir para GitHub
2. [ ] Escolher plataforma de deploy
3. [ ] Fazer deploy
4. [ ] Popular banco
5. [ ] Testar online
6. [ ] Compartilhar link
7. [ ] Adicionar ao portfólio
8. [ ] Divulgar nas redes

**Boa sorte! 🚀**
