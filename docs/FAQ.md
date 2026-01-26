# FAQ - Perguntas Frequentes

## Geral

### O que é o Sistema de Simulados IBGP?
É uma plataforma completa de treino adaptativo para concursos públicos, focada no cargo de Técnico em Informática com questões no estilo da banca IBGP.

### É gratuito?
Sim, o projeto é open-source sob licença MIT.

### Posso usar para outras bancas?
Sim, o sistema é configurável. Você pode adaptar os templates de questões para outras bancas.

## Instalação

### Quais são os requisitos?
- Docker e Docker Compose
- Git
- 4GB RAM mínimo
- 10GB espaço em disco

### Como instalo?
Veja o [Quickstart Guide](QUICKSTART.md).

### Funciona no Windows?
Sim, com Docker Desktop instalado.

### Funciona no Mac?
Sim, com Docker Desktop instalado.

## Uso

### Como faço upload de um edital?
1. Acesse "Upload Edital"
2. Selecione arquivo TXT ou PDF
3. Aguarde processamento
4. Veja mensagem: "Conteúdo programático recebido"

### Quantas questões são geradas?
- Tópicos amplos: mínimo 30 questões
- Tópicos pequenos: mínimo 10 questões
- Configurável via API

### Como funcionam os simulados?
1. Crie um simulado (configure questões, tempo, disciplinas)
2. Execute respondendo as questões
3. Receba feedback imediato
4. Finalize e veja relatório completo

### O que é treino adaptativo?
Sistema que prioriza questões baseado no seu desempenho:
- Tópicos com <60% acerto têm prioridade
- Questões erradas são revisadas com espaçamento (SRS)
- Plano de estudo personalizado

### Como funciona o SRS?
Spaced Repetition System:
- Questões corretas: intervalo aumenta exponencialmente
- Questões erradas: revisão imediata
- Baseado em curva de esquecimento

## Questões

### Como adiciono questões manualmente?
Via API:
```bash
POST /api/questions
{
  "disciplina": "Hardware",
  "topico": "Memórias",
  ...
}
```

### Como valido questões?
```bash
docker-compose exec api python scripts/validate_questions.py
```

### O que é QA score?
Pontuação de qualidade (0-100) baseada em:
- Verificação factual
- Consistência linguística
- Claridade
- Qualidade das alternativas
- Explicação adequada

### Questões com score baixo são usadas?
- Score >= 80: Aprovadas automaticamente
- Score 60-79: Requerem revisão
- Score < 60: Rejeitadas

## Desenvolvimento

### Como contribuo?
Veja [CONTRIBUTING.md](../CONTRIBUTING.md).

### Como reporto bugs?
Use o template de Bug Report nas Issues.

### Como sugiro funcionalidades?
Use o template de Feature Request nas Issues.

### Como rodo os testes?
```bash
# API
docker-compose exec api pytest tests/ -v

# Web
docker-compose exec web npm test
```

## Deploy

### Como faço deploy em produção?
Veja [DEPLOYMENT.md](DEPLOYMENT.md).

### Posso usar em servidor compartilhado?
Recomendamos VPS com Docker instalado.

### Preciso de SSL?
Sim, para produção use Certbot (Let's Encrypt).

### Como faço backup?
```bash
docker-compose exec postgres pg_dump -U simulados_user simulados_db > backup.sql
```

## Performance

### Quantos usuários simultâneos suporta?
Depende do servidor. Com 2GB RAM: ~50 usuários.

### Como otimizo?
- Use Redis para cache
- Configure índices no banco
- Use CDN para assets estáticos
- Implemente rate limiting

### Posso escalar horizontalmente?
Sim, a API é stateless. Use load balancer.

## Segurança

### É seguro?
Sim, implementa:
- JWT authentication
- Hashing de senhas (bcrypt)
- Validação de inputs
- CORS configurável

### Como protejo em produção?
- Use HTTPS
- Configure SECRET_KEY forte
- Use senhas fortes
- Configure firewall
- Mantenha sistema atualizado

## Dados

### Onde ficam os dados?
- PostgreSQL: questões, usuários, resultados
- Redis: cache, sessões
- Volumes Docker: persistência

### Como exporto dados?
Via API:
- GIFT: `/api/export/gift`
- CSV: `/api/export/csv`
- JSON: `/api/export/json`

### Posso importar questões?
Sim, via API ou diretamente no banco.

## Troubleshooting

### Container não inicia
```bash
docker-compose down -v
docker-compose up --build
```

### Erro de conexão com banco
```bash
docker-compose logs postgres
docker-compose restart postgres
```

### Porta já em uso
Altere portas no `docker-compose.yml`.

### Erro de permissão
```bash
sudo chown -R $USER:$USER .
```

## Suporte

### Onde peço ajuda?
- GitHub Issues
- GitHub Discussions
- Email: [seu-email]

### Há documentação adicional?
Sim, em `/docs`:
- [API.md](API.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [DEPLOYMENT.md](DEPLOYMENT.md)
- [QUICKSTART.md](QUICKSTART.md)

### Posso contratar suporte?
Contate os mantenedores do projeto.
