# 🚀 Como Testar o Sistema - Guia Rápido

## 📋 Opções de Teste

Escolha uma das opções abaixo:

### 🎯 Opção 1: Teste Automatizado Completo (Recomendado)

Execute o script Python que testa todo o fluxo:

```bash
# Instalar dependências
pip install requests

# Executar teste completo
python test_complete_flow.py
```

**O que testa:**
- ✅ Health check
- ✅ Login
- ✅ Importar questões reais
- ✅ Listar questões
- ✅ Upload de edital
- ✅ Listar tópicos
- ✅ Estatísticas do Gemini
- ✅ Gerar questões com IA
- ✅ Criar simulado
- ✅ Listar simulados

**Resultado esperado:**
```
🎉 TODOS OS TESTES PASSARAM!
   Sistema está funcionando corretamente!
```

---

### 🛡️ Opção 2: Teste de Rate Limiting

Testa se o sistema bloqueia corretamente após 55 requisições/minuto:

```bash
python test_rate_limit.py
```

**O que testa:**
- ✅ Faz 60 requisições rápidas
- ✅ Verifica se bloqueia na 56ª
- ✅ Mostra estatísticas de uso
- ✅ Confirma que rate limiting funciona

**Resultado esperado:**
```
🎉 TESTE COMPLETO: PASSOU
   Rate limiting está funcionando corretamente!
```

---

### 🖱️ Opção 3: Teste Manual via Interface

1. **Iniciar sistema:**
   ```bash
   # Terminal 1 - API
   cd api
   uvicorn main:app --reload

   # Terminal 2 - Frontend
   cd web
   npm run dev
   ```

2. **Acessar:** http://localhost:3000

3. **Seguir fluxo:**
   - Login: `teste` / `teste123`
   - Ir em "🤖 IA Questões"
   - Importar `data/exemplo_prova.txt`
   - Gerar questões com IA
   - Criar e executar simulado

---

### 📝 Opção 4: Teste Manual via API (Swagger)

1. **Acessar:** http://localhost:8000/docs

2. **Testar endpoints:**
   - `POST /api/token` - Login
   - `POST /api/import-questions` - Importar
   - `GET /api/gemini-stats` - Estatísticas
   - `POST /api/generate-with-ai` - Gerar IA

---

## 🔧 Preparação (Primeira Vez)

### 1. Instalar Dependências

```bash
# API
cd api
pip install -r requirements.txt

# Frontend
cd web
npm install
```

### 2. Configurar .env

```bash
# Copiar exemplo
copy .env.example .env

# Editar e adicionar chave do Gemini
# GEMINI_API_KEY=AIzaSyDVkUtP5CEkec1Du0nNA8h0ERoOsVG6g-w
```

### 3. Iniciar Banco de Dados

```bash
docker-compose up -d postgres
```

### 4. Criar Usuário de Teste

```bash
curl -X POST http://localhost:8000/api/seed-simple
```

---

## ✅ Checklist Rápido

Antes de fazer deploy, verificar:

- [ ] `python test_complete_flow.py` → Todos passam
- [ ] `python test_rate_limit.py` → Rate limiting funciona
- [ ] Interface carrega sem erros
- [ ] Login funciona
- [ ] Importar questões funciona
- [ ] Gerar com IA funciona
- [ ] Criar simulado funciona
- [ ] Executar simulado funciona

---

## 🌐 Testar em Produção

Após deploy no Render:

```bash
# Testar API
curl https://simulados-ibgp.onrender.com/health

# Testar Frontend
start https://simulados-ibgp-1.onrender.com
```

---

## 📚 Documentação Completa

Para testes detalhados, consulte:

- **TESTE_AUTOMATIZADO.md** - 36 tasks de teste
- **TESTE_GEMINI.md** - Testes específicos da IA
- **docs/RATE_LIMITING.md** - Detalhes do rate limiting

---

## 🆘 Problemas Comuns

### Erro: "Connection refused"
```bash
# Verificar se API está rodando
netstat -ano | findstr :8000
```

### Erro: "GEMINI_API_KEY não configurada"
```bash
# Verificar .env
type .env | findstr GEMINI
```

### Erro: "No topics found"
```bash
# Fazer upload de edital primeiro
curl -X POST http://localhost:8000/api/upload-syllabus -F "file=@test_edital.txt"
```

---

## 🎉 Sucesso!

Se todos os testes passaram, o sistema está pronto para produção! 🚀
