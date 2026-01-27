# 🧪 Guia de Testes Automatizados - Sistema Completo

Este guia contém todos os comandos e scripts para testar o sistema de ponta a ponta.

## 📋 Índice

- [Preparação do Ambiente](#preparação-do-ambiente)
- [Testes da API](#testes-da-api)
- [Testes do Frontend](#testes-do-frontend)
- [Testes de Integração](#testes-de-integração)
- [Testes de Rate Limiting](#testes-de-rate-limiting)
- [Testes em Produção](#testes-em-produção)

---

## 🚀 Preparação do Ambiente

### Task 1: Setup Inicial

```bash
# Clone e entre no diretório
git clone https://github.com/Dev-HP/simulados-ibgp.git
cd simulados-ibgp

# Copiar .env de exemplo
copy .env.example .env

# Editar .env e adicionar chave do Gemini
# GEMINI_API_KEY=AIzaSyDVkUtP5CEkec1Du0nNA8h0ERoOsVG6g-w
```

### Task 2: Instalar Dependências

```bash
# API
cd api
pip install -r requirements.txt
cd ..

# Frontend
cd web
npm install
cd ..
```

### Task 3: Iniciar Banco de Dados

```bash
# Iniciar PostgreSQL com Docker
docker-compose up -d postgres

# Aguardar 5 segundos
timeout /t 5

# Verificar se está rodando
docker ps | findstr postgres
```

**Resultado esperado:**
```
✅ Container postgres rodando na porta 5432
```

---

## 🔧 Testes da API

### Task 4: Iniciar API

```bash
# Terminal 1
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Aguarde ver:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Task 5: Testar Health Check

```bash
# Terminal 2
curl http://localhost:8000/health
```

**Resultado esperado:**
```json
{"status":"healthy"}
```

### Task 6: Testar Documentação

```bash
# Abrir no navegador
start http://localhost:8000/docs
```

**Verificar:**
- ✅ Swagger UI carrega
- ✅ Todos os endpoints aparecem
- ✅ Schemas estão corretos

### Task 7: Criar Usuário de Teste

```bash
curl -X POST http://localhost:8000/api/seed-simple
```

**Resultado esperado:**
```json
{
  "status": "success",
  "message": "Usuário criado!",
  "credentials": {
    "username": "teste",
    "password": "teste123"
  }
}
```

### Task 8: Testar Login

```bash
curl -X POST http://localhost:8000/api/token ^
  -H "Content-Type: application/x-www-form-urlencoded" ^
  -d "username=teste&password=teste123"
```

**Resultado esperado:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Task 9: Importar Questões Reais

```bash
curl -X POST http://localhost:8000/api/import-questions ^
  -H "Authorization: Bearer SEU_TOKEN_AQUI" ^
  -F "file=@data/exemplo_prova.txt" ^
  -F "disciplina=Informática"
```

**Resultado esperado:**
```json
{
  "message": "Questions imported successfully",
  "total_imported": 10,
  "source": "exemplo_prova.txt"
}
```

### Task 10: Listar Questões Importadas

```bash
curl http://localhost:8000/api/questions?limit=20
```

**Verificar:**
- ✅ 10 questões retornadas
- ✅ Cada questão tem enunciado, alternativas, gabarito
- ✅ Disciplina = "Informática"

### Task 11: Upload de Edital

Criar arquivo `test_edital.txt`:
```
HARDWARE
1. Componentes de hardware
2. Memória RAM e ROM

REDES
1. Protocolos TCP/IP
2. Modelo OSI
```

```bash
curl -X POST http://localhost:8000/api/upload-syllabus ^
  -H "Authorization: Bearer SEU_TOKEN_AQUI" ^
  -F "file=@test_edital.txt"
```

**Resultado esperado:**
```json
{
  "message": "Conteúdo programático recebido",
  "id": 1,
  "filename": "test_edital.txt"
}
```

### Task 12: Listar Tópicos

```bash
curl http://localhost:8000/api/topics
```

**Verificar:**
- ✅ Tópicos extraídos do edital
- ✅ Disciplinas corretas
- ✅ Referências às linhas

### Task 13: Verificar Status do Gemini

```bash
curl http://localhost:8000/api/gemini-stats
```

**Resultado esperado:**
```json
{
  "status": "ok",
  "tier": "free",
  "limits": {
    "per_minute": 55,
    "per_day": 1400
  },
  "usage": {
    "last_minute": 0,
    "today": 0,
    "total": 0,
    "blocked": 0
  },
  "remaining": {
    "minute": 55,
    "day": 1400
  }
}
```

### Task 14: Gerar Questões com IA

```bash
curl -X POST "http://localhost:8000/api/generate-with-ai?topic_id=1&quantity=5&difficulty=MEDIO&use_references=true" ^
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Resultado esperado:**
```json
{
  "message": "Questions generated with AI successfully",
  "total_generated": 5,
  "topic": "Componentes de hardware",
  "references_used": 10
}
```

### Task 15: Verificar Rate Limiting

```bash
# Fazer 60 requisições rápidas para testar bloqueio
for /L %i in (1,1,60) do curl -X POST "http://localhost:8000/api/generate-with-ai?topic_id=1&quantity=1" -H "Authorization: Bearer SEU_TOKEN"
```

**Resultado esperado:**
```
✅ Primeiras 55 requisições: sucesso
❌ Requisições 56-60: erro 429
{
  "detail": "Limite de 55 requisições/minuto atingido. Aguarde Xs."
}
```

### Task 16: Criar Simulado

```bash
curl -X POST http://localhost:8000/api/create-simulado ^
  -H "Authorization: Bearer SEU_TOKEN_AQUI" ^
  -H "Content-Type: application/json" ^
  -d "{\"nome\":\"Teste Automatizado\",\"numero_questoes\":5,\"tempo_total\":15}"
```

**Resultado esperado:**
```json
{
  "id": 1,
  "nome": "Teste Automatizado",
  "numero_questoes": 5,
  "tempo_total": 15
}
```

### Task 17: Listar Simulados

```bash
curl http://localhost:8000/api/simulados
```

**Verificar:**
- ✅ Simulado criado aparece
- ✅ Dados corretos

---

## 🎨 Testes do Frontend

### Task 18: Iniciar Frontend

```bash
# Terminal 3
cd web
npm run dev
```

**Aguarde ver:**
```
VITE ready in XXXms
Local: http://localhost:3000
```

### Task 19: Testar Página de Login

```bash
# Abrir no navegador
start http://localhost:3000
```

**Verificar:**
- ✅ Página de login carrega
- ✅ Campos de usuário e senha aparecem
- ✅ Credenciais de teste visíveis
- ✅ Sem erros no console

### Task 20: Fazer Login

**Manual:**
1. Usuário: `teste`
2. Senha: `teste123`
3. Clicar em "Entrar"

**Verificar:**
- ✅ Redireciona para Home
- ✅ Menu de navegação aparece
- ✅ Botão "Sair (teste)" visível
- ✅ Token salvo no localStorage

### Task 21: Testar Navegação

**Clicar em cada menu:**
- ✅ Home → Carrega
- ✅ Upload Edital → Carrega
- ✅ 🤖 IA Generator → Carrega
- ✅ Simulados → Carrega
- ✅ Analytics → Carrega

**Verificar:**
- ✅ Nenhuma página recarrega (SPA)
- ✅ URL muda corretamente
- ✅ Sem erros no console

### Task 22: Testar Upload de Edital

1. Ir em "Upload Edital"
2. Selecionar arquivo `test_edital.txt`
3. Clicar em "Upload"

**Verificar:**
- ✅ Mensagem de sucesso aparece
- ✅ "Conteúdo programático recebido e banco de questões gerado!"

### Task 23: Testar Importação de Questões

1. Ir em "🤖 IA Generator"
2. Aba "📥 Importar Questões Reais"
3. Selecionar `data/exemplo_prova.txt`
4. Disciplina: "Informática"
5. Clicar em "Importar Questões"

**Verificar:**
- ✅ Mensagem: "✅ 10 questões importadas com sucesso!"
- ✅ Estatísticas atualizam
- ✅ Total de questões aumenta

### Task 24: Verificar Dashboard de Estatísticas

**Na página "🤖 IA Generator":**

**Verificar:**
- ✅ "Total de Questões" mostra número correto
- ✅ "Informática" mostra 10 questões
- ✅ Status do Gemini aparece
- ✅ Barras de progresso funcionam
- ✅ "Limite por Minuto" mostra uso
- ✅ "Limite Diário" mostra uso

### Task 25: Testar Geração com IA

1. Aba "🤖 Gerar com IA"
2. Selecionar tópico: "Hardware - Componentes de hardware"
3. Quantidade: 5
4. Dificuldade: Médio
5. Marcar "Usar questões reais como referência"
6. Clicar em "Gerar Questões"

**Verificar:**
- ✅ Botão muda para "⏳ Gerando com IA..."
- ✅ Aguarda ~15-30 segundos
- ✅ Mensagem: "✅ 5 questões geradas com IA!"
- ✅ Estatísticas atualizam
- ✅ Total aumenta para 15 questões

### Task 26: Testar Criação de Simulado

1. Ir em "Simulados"
2. Clicar em "Criar Simulado"
3. Nome: "Teste Frontend"
4. Questões: 5
5. Tempo: 15 minutos
6. Clicar em "Criar"

**Verificar:**
- ✅ Simulado aparece na lista
- ✅ Botão "Iniciar" visível

### Task 27: Testar Execução de Simulado

1. Clicar em "Iniciar" no simulado criado
2. Ler questão
3. Selecionar uma alternativa
4. Clicar em "Responder"

**Verificar:**
- ✅ Questão carrega corretamente
- ✅ 4 alternativas aparecem
- ✅ Alternativa selecionada destaca
- ✅ Feedback aparece após responder
- ✅ Explicação é mostrada
- ✅ Botão "Próxima Questão" aparece
- ✅ Contador de questões funciona

### Task 28: Testar Logout

1. Clicar em "Sair (teste)"

**Verificar:**
- ✅ Redireciona para login
- ✅ Token removido do localStorage
- ✅ Não consegue acessar páginas protegidas

---

## 🔗 Testes de Integração

### Task 29: Fluxo Completo End-to-End

**Script automatizado:**

```bash
# 1. Login
curl -X POST http://localhost:8000/api/token ^
  -d "username=teste&password=teste123" > token.json

# 2. Extrair token
# (usar jq ou manualmente)

# 3. Importar questões
curl -X POST http://localhost:8000/api/import-questions ^
  -H "Authorization: Bearer TOKEN" ^
  -F "file=@data/exemplo_prova.txt"

# 4. Upload edital
curl -X POST http://localhost:8000/api/upload-syllabus ^
  -H "Authorization: Bearer TOKEN" ^
  -F "file=@test_edital.txt"

# 5. Gerar com IA
curl -X POST "http://localhost:8000/api/generate-with-ai?topic_id=1&quantity=5" ^
  -H "Authorization: Bearer TOKEN"

# 6. Criar simulado
curl -X POST http://localhost:8000/api/create-simulado ^
  -H "Authorization: Bearer TOKEN" ^
  -d "{\"nome\":\"Auto\",\"numero_questoes\":5,\"tempo_total\":15}"

# 7. Listar questões do simulado
curl http://localhost:8000/api/simulados/1
```

**Verificar:**
- ✅ Todos os passos executam sem erro
- ✅ Dados persistem no banco
- ✅ Questões geradas têm qualidade

---

## 🛡️ Testes de Rate Limiting

### Task 30: Testar Limite por Minuto

```python
# Script Python: test_rate_limit.py
import requests
import time

API_URL = "http://localhost:8000"
TOKEN = "SEU_TOKEN_AQUI"

headers = {"Authorization": f"Bearer {TOKEN}"}

print("Testando limite de 55 req/min...")
for i in range(60):
    response = requests.post(
        f"{API_URL}/api/generate-with-ai",
        params={"topic_id": 1, "quantity": 1},
        headers=headers
    )
    
    if response.status_code == 429:
        print(f"✅ Bloqueado na requisição {i+1}")
        print(f"Mensagem: {response.json()['detail']}")
        break
    elif response.status_code == 200:
        print(f"Requisição {i+1}: OK")
    else:
        print(f"Erro inesperado: {response.status_code}")
        break
    
    time.sleep(0.5)
```

**Executar:**
```bash
python test_rate_limit.py
```

**Resultado esperado:**
```
Requisição 1: OK
Requisição 2: OK
...
Requisição 55: OK
✅ Bloqueado na requisição 56
Mensagem: Limite de 55 requisições/minuto atingido. Aguarde 45s.
```

### Task 31: Verificar Estatísticas Após Bloqueio

```bash
curl http://localhost:8000/api/gemini-stats
```

**Verificar:**
- ✅ `usage.last_minute` = 55
- ✅ `remaining.minute` = 0
- ✅ `usage.blocked` > 0
- ✅ `percentage.minute` = 100

### Task 32: Aguardar Reset e Testar Novamente

```bash
# Aguardar 60 segundos
timeout /t 60

# Tentar novamente
curl -X POST "http://localhost:8000/api/generate-with-ai?topic_id=1&quantity=1" ^
  -H "Authorization: Bearer TOKEN"
```

**Resultado esperado:**
```
✅ Requisição funciona novamente
✅ Contador resetou
```

---

## 🌐 Testes em Produção (Render)

### Task 33: Configurar Gemini no Render

1. Acessar: https://dashboard.render.com
2. Selecionar serviço: `simulados-ibgp`
3. Environment → Add Environment Variable
4. Key: `GEMINI_API_KEY`
5. Value: `AIzaSyDVkUtP5CEkec1Du0nNA8h0ERoOsVG6g-w`
6. Save Changes
7. Aguardar redeploy (~3-5 min)

### Task 34: Testar API em Produção

```bash
# Health check
curl https://simulados-ibgp.onrender.com/health

# Docs
start https://simulados-ibgp.onrender.com/docs

# Gemini stats
curl https://simulados-ibgp.onrender.com/api/gemini-stats
```

### Task 35: Testar Frontend em Produção

```bash
start https://simulados-ibgp-1.onrender.com
```

**Verificar:**
1. ✅ Login funciona
2. ✅ Navegação funciona
3. ✅ Importar questões funciona
4. ✅ Gerar com IA funciona
5. ✅ Criar simulado funciona
6. ✅ Executar simulado funciona
7. ✅ Rate limiting funciona
8. ✅ Dashboard de estatísticas funciona

### Task 36: Teste de Carga

```python
# Script: load_test.py
import requests
import concurrent.futures
import time

API_URL = "https://simulados-ibgp.onrender.com"

def make_request(i):
    try:
        response = requests.get(f"{API_URL}/health")
        return f"Request {i}: {response.status_code}"
    except Exception as e:
        return f"Request {i}: Error - {str(e)}"

print("Teste de carga: 100 requisições simultâneas...")
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(make_request, i) for i in range(100)]
    for future in concurrent.futures.as_completed(futures):
        print(future.result())
```

**Executar:**
```bash
python load_test.py
```

**Verificar:**
- ✅ Todas as requisições respondem
- ✅ Tempo de resposta < 2s
- ✅ Sem erros 500

---

## ✅ Checklist Final

### API
- [ ] Health check funciona
- [ ] Documentação carrega
- [ ] Login funciona
- [ ] Importar questões funciona
- [ ] Upload edital funciona
- [ ] Gerar com IA funciona
- [ ] Rate limiting funciona
- [ ] Estatísticas funcionam
- [ ] Criar simulado funciona

### Frontend
- [ ] Login funciona
- [ ] Navegação funciona (SPA)
- [ ] Upload edital funciona
- [ ] Importar questões funciona
- [ ] Gerar com IA funciona
- [ ] Dashboard de estatísticas funciona
- [ ] Criar simulado funciona
- [ ] Executar simulado funciona
- [ ] Logout funciona

### Integração
- [ ] Fluxo completo funciona
- [ ] Dados persistem
- [ ] Questões têm qualidade
- [ ] Rate limiting protege API

### Produção
- [ ] Deploy no Render funciona
- [ ] Gemini configurado
- [ ] Tudo funciona em produção
- [ ] Performance adequada

---

## 📊 Relatório de Testes

Após executar todos os testes, preencher:

```
Data: ___/___/___
Testador: ___________

RESULTADOS:
- Total de testes: 36
- Passou: ___
- Falhou: ___
- Pulado: ___

PROBLEMAS ENCONTRADOS:
1. _______________
2. _______________
3. _______________

OBSERVAÇÕES:
_______________
_______________
_______________

STATUS FINAL: [ ] APROVADO  [ ] REPROVADO
```

---

## 🆘 Troubleshooting Rápido

### Erro: "Connection refused"
```bash
# Verificar se serviço está rodando
netstat -ano | findstr :8000
```

### Erro: "GEMINI_API_KEY não configurada"
```bash
# Verificar .env
type .env | findstr GEMINI
```

### Erro: "Rate limit exceeded"
```bash
# Aguardar 60 segundos
timeout /t 60
```

### Erro: "No topics found"
```bash
# Fazer upload de edital primeiro
curl -X POST http://localhost:8000/api/upload-syllabus -F "file=@test_edital.txt"
```

---

## 🎉 Conclusão

Se todos os 36 testes passaram, o sistema está **100% funcional** e pronto para uso em produção!
