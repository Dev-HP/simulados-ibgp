# Guia de Deploy

## Deploy Local (Desenvolvimento)

### Pré-requisitos
- Docker e Docker Compose instalados
- Git

### Passos

1. Clone o repositório:
```bash
git clone <repo-url>
cd simulados-ibgp
```

2. Configure variáveis de ambiente:
```bash
cp .env.example .env
# Edite .env com suas configurações
```

3. Inicie os containers:
```bash
docker-compose up --build
```

4. Acesse:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

5. Popule o banco (opcional):
```bash
docker-compose exec api python scripts/seed_database.py
```

## Deploy em Produção

### Opção 1: VPS (DigitalOcean, AWS EC2, etc)

1. Provisione um servidor Ubuntu 22.04+

2. Instale Docker:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

3. Clone e configure:
```bash
git clone <repo-url>
cd simulados-ibgp
cp .env.example .env
nano .env  # Configure para produção
```

4. Configure variáveis de produção:
```env
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=<gerar-chave-segura>
POSTGRES_PASSWORD=<senha-forte>
```

5. Inicie:
```bash
docker-compose up -d
```

6. Configure SSL com Certbot (opcional):
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com
```

### Opção 2: GitHub Container Registry + Cloud Run

1. Build e push das imagens:
```bash
docker build -t ghcr.io/seu-usuario/simulados-api:latest -f docker/Dockerfile.api ./api
docker build -t ghcr.io/seu-usuario/simulados-web:latest -f docker/Dockerfile.web ./web

docker push ghcr.io/seu-usuario/simulados-api:latest
docker push ghcr.io/seu-usuario/simulados-web:latest
```

2. Deploy no Cloud Run (Google Cloud):
```bash
gcloud run deploy simulados-api \
  --image ghcr.io/seu-usuario/simulados-api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

gcloud run deploy simulados-web \
  --image ghcr.io/seu-usuario/simulados-web:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Opção 3: Heroku

1. Instale Heroku CLI

2. Crie apps:
```bash
heroku create simulados-api
heroku create simulados-web
```

3. Configure buildpacks:
```bash
heroku buildpacks:set heroku/python -a simulados-api
heroku buildpacks:set heroku/nodejs -a simulados-web
```

4. Configure variáveis:
```bash
heroku config:set SECRET_KEY=<chave> -a simulados-api
heroku config:set DATABASE_URL=<postgres-url> -a simulados-api
```

5. Deploy:
```bash
git push heroku main
```

## Backup e Restore

### Backup do PostgreSQL
```bash
docker-compose exec postgres pg_dump -U simulados_user simulados_db > backup.sql
```

### Restore
```bash
docker-compose exec -T postgres psql -U simulados_user simulados_db < backup.sql
```

## Monitoramento

### Logs
```bash
# Todos os serviços
docker-compose logs -f

# Apenas API
docker-compose logs -f api

# Apenas Web
docker-compose logs -f web
```

### Health Checks
```bash
# API
curl http://localhost:8000/health

# Database
docker-compose exec postgres pg_isready
```

## Troubleshooting

### Container não inicia
```bash
docker-compose down -v
docker-compose up --build
```

### Erro de conexão com banco
Verifique se o PostgreSQL está rodando:
```bash
docker-compose ps
docker-compose logs postgres
```

### Porta já em uso
Altere as portas no docker-compose.yml ou pare o serviço conflitante.

## Segurança em Produção

1. **Sempre use HTTPS**
2. **Configure SECRET_KEY forte**
3. **Use senhas fortes para banco**
4. **Configure firewall (UFW)**:
```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```
5. **Mantenha sistema atualizado**
6. **Configure backups automáticos**
7. **Use rate limiting**
8. **Configure CORS adequadamente**
