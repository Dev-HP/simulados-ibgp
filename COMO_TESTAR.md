# 🚀 Como Testar o Sistema - Guia Rápido

## 🎯 Teste Automatizado Completo (RECOMENDADO)

### Opção 1: Script Master - Executa TUDO Automaticamente

Este é o jeito mais fácil! Um único comando executa todos os testes:

```bash
# Instalar dependências (primeira vez)
pip install requests

# Executar TODOS os testes
python run_all_tests.py
```

**O que faz:**
1. ✅ Verifica pré-requisitos (Python, Node, Docker, etc)
2. ✅ Verifica se serviços estão rodando
3. ✅ Executa 8 testes básicos da API
4. ✅ Executa teste completo do fluxo (10 testes)
5. ✅ Executa teste de rate limiting (opcional)
6. ✅ Gera relatório detalhado
7. ✅ Salva relatório em arquivo

**Resultado esperado:**
```
🎉 TODOS OS TESTES PASSARAM!
   Sistema está funcionando perfeitamente!

Relatório salvo em: test_report_20260127_120000.txt
```

---

## 📋 Outras Opções de Teste

### Opção 2: Teste Completo do Fluxo

Testa todo o fluxo end-to-end (sem rate limiting):

```bash
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

### Opção 3: Teste de Rate Limiting

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

### Opção 4: Teste Manual via Interface

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

### Opção 5: Teste Manual via API (Swagger)

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

# Testes
pip install requests
```

### 2. Configurar .env

```bash
# Copiar exemplo
copy .env.example .env

# Editar e adicionar chave do Gemini
# GEMINI_API_KEY=[SUA_CHAVE_AQUI]
```

### 3. Iniciar Banco de Dados

```bash
docker-compose up -d postgres
```

### 4. Iniciar Serviços

```bash
# Terminal 1 - API
cd api
uvicorn main:app --reload

# Terminal 2 - Frontend (opcional)
cd web
npm run dev
```

### 5. Executar Testes

```bash
# Terminal 3
python run_all_tests.py
```

---

## ✅ Checklist Rápido

Antes de fazer deploy, verificar:

- [ ] `python run_all_tests.py` → Todos passam
- [ ] Relatório gerado sem erros
- [ ] Interface carrega sem erros
- [ ] Login funciona
- [ ] Importar questões funciona
- [ ] Gerar com IA funciona
- [ ] Criar simulado funciona
- [ ] Executar simulado funciona

---

## 📊 Entendendo o Relatório

O script `run_all_tests.py` gera um relatório como este:

```
================================================================================
                        RELATÓRIO FINAL DE TESTES
================================================================================

Resumo Geral:
  Total de testes: 19
  Passaram: 19
  Falharam: 0
  Taxa de sucesso: 100.0%

Detalhes por Categoria:

  ✅ Testes da API (Básicos)........................... 8/8 (100%)
  ✅ Teste Completo (E2E).............................. 1/1 (100%)
  ✅ Teste de Rate Limiting............................ 1/1 (100%)

📄 Relatório salvo em: test_report_20260127_120000.txt
```

**Legenda:**
- ✅ = Todos os testes passaram
- ⚠️ = Alguns testes passaram
- ❌ = Todos os testes falharam

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

- **TESTE_AUTOMATIZADO.md** - 36 tasks de teste manual
- **TESTE_GEMINI.md** - Testes específicos da IA
- **docs/RATE_LIMITING.md** - Detalhes do rate limiting

---

## 🆘 Problemas Comuns

### Erro: "API não está rodando"
```bash
# Iniciar API
cd api
uvicorn main:app --reload
```

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

### Erro: "Module 'requests' not found"
```bash
# Instalar requests
pip install requests
```

---

## 🎯 Fluxo Recomendado

**Para desenvolvimento:**
```bash
1. Iniciar serviços (API + Frontend)
2. python run_all_tests.py
3. Corrigir erros se houver
4. Repetir até 100% passar
```

**Para deploy:**
```bash
1. python run_all_tests.py → 100% passar
2. git commit e push
3. Configurar GEMINI_API_KEY no Render
4. Aguardar deploy
5. Testar em produção
```

---

## 🎉 Sucesso!

Se `python run_all_tests.py` mostrar:

```
🎉 TODOS OS TESTES PASSARAM!
   Sistema está funcionando perfeitamente!
```

O sistema está **100% pronto** para produção! 🚀
