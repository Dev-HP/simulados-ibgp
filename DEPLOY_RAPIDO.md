# 🚀 Deploy Rápido - 3 Passos

## Passo 1: Subir para GitHub (5 minutos)

### Windows
```bash
setup_github.bat
```

### Linux/Mac
```bash
bash setup_github.sh
```

**OU manualmente:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/SEU-USUARIO/simulados-ibgp.git
git push -u origin main
```

✅ **Resultado**: Código no GitHub!

---

## Passo 2: Deploy Online (10 minutos)

### 🎯 Render.com (MAIS FÁCIL)

1. **Criar conta**: https://render.com
2. **Conectar GitHub**: Autorize acesso ao repositório
3. **Deploy Backend**:
   - New + → Web Service
   - Selecione repositório
   - Environment: Docker
   - Dockerfile: `docker/Dockerfile.api`
   - Clique "Create"

4. **Criar PostgreSQL**:
   - New + → PostgreSQL
   - Free plan
   - Copie URL de conexão

5. **Deploy Frontend**:
   - New + → Static Site
   - Build: `cd web && npm install && npm run build`
   - Publish: `web/dist`
   - Clique "Create"

6. **Configurar Variáveis**:
   - No backend, adicione:
     ```
     POSTGRES_HOST=<do-postgres>
     POSTGRES_DB=simulados_db
     POSTGRES_USER=simulados_user
     POSTGRES_PASSWORD=<senha>
     SECRET_KEY=<gerar-aleatoria>
     ```

✅ **Resultado**: Sistema online em ~10 minutos!

**URLs geradas**:
- Frontend: `https://simulados-web.onrender.com`
- API: `https://simulados-api.onrender.com`

---

### 🎯 Railway.app (MAIS RÁPIDO)

1. **Criar conta**: https://railway.app
2. **Deploy**:
   - "Deploy from GitHub repo"
   - Selecione `simulados-ibgp`
   - Railway detecta docker-compose
   - Clique "Deploy"

3. **Configurar Variáveis**:
   - Clique em cada serviço
   - Adicione variáveis do `.env.example`

✅ **Resultado**: Deploy automático em ~5 minutos!

---

### 🎯 Fly.io (MAIS RÁPIDO GLOBALMENTE)

```bash
# Instalar CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Deploy API
cd api
fly launch --name simulados-api

# Deploy Web
cd ../web
fly launch --name simulados-web

# Criar PostgreSQL
fly postgres create --name simulados-db
fly postgres attach simulados-db -a simulados-api
```

✅ **Resultado**: Deploy global em ~5 minutos!

---

## Passo 3: Popular e Testar (2 minutos)

### Popular Banco de Dados

**Render.com**:
1. Dashboard → simulados-api → Shell
2. Execute: `python scripts/seed_database.py`

**Railway**:
```bash
railway run python scripts/seed_database.py
```

**Fly.io**:
```bash
fly ssh console -a simulados-api
python scripts/seed_database.py
```

### Testar Sistema

1. Acesse o frontend (URL gerada)
2. Login: `teste` / `senha123`
3. Upload edital: `data/pasted_content.txt`
4. Gere banco de questões
5. Crie e execute simulado

✅ **Resultado**: Sistema funcionando online!

---

## 🎉 Pronto! Sistema Online

### Compartilhe:

**Seu link**: `https://seu-app.onrender.com`

**Adicione ao README**:
```markdown
## 🌐 Demo Online

Acesse: https://seu-app.onrender.com

Credenciais de teste:
- Username: `teste`
- Password: `senha123`
```

### Divulgue:
- ✅ LinkedIn
- ✅ Twitter
- ✅ GitHub README
- ✅ Portfólio
- ✅ Grupos de concursos
- ✅ Comunidades de dev

---

## 📊 Comparação de Plataformas

| Plataforma | Facilidade | Velocidade | Gratuito | Recomendado |
|------------|-----------|-----------|----------|-------------|
| **Render.com** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ✅ Sim |
| **Railway.app** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ✅ Sim |
| **Fly.io** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | Para avançados |
| **Heroku** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | Clássico |

---

## 🆘 Problemas Comuns

### "Build failed"
- Verifique Dockerfile paths
- Confirme variáveis de ambiente
- Veja logs no dashboard

### "Cannot connect to database"
- Verifique DATABASE_URL
- Confirme PostgreSQL está rodando
- Teste conexão manualmente

### "Frontend não carrega"
- Verifique VITE_API_URL
- Confirme CORS no backend
- Rebuild do frontend

---

## 📚 Documentação Completa

- **Detalhes completos**: [GITHUB_SETUP.md](GITHUB_SETUP.md)
- **Opções avançadas**: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **Troubleshooting**: [docs/FAQ.md](docs/FAQ.md)

---

## ⏱️ Tempo Total

- ✅ GitHub: 5 minutos
- ✅ Deploy: 10 minutos
- ✅ Testar: 2 minutos

**Total: ~17 minutos do zero ao online!**

---

## 🎯 Checklist Final

- [ ] Código no GitHub
- [ ] Deploy realizado
- [ ] Banco populado
- [ ] Sistema testado
- [ ] Link funcionando
- [ ] README atualizado com link
- [ ] Compartilhado nas redes

---

**Boa sorte! 🚀**

Qualquer dúvida, veja a documentação completa ou abra uma issue no GitHub.
