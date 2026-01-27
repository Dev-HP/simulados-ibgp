# 🧪 Guia de Teste - Gemini AI Integration

Este guia mostra como testar o sistema completo com geração de questões por IA.

## 📋 Pré-requisitos

- Python 3.11+
- Node.js 18+
- Docker Desktop (para PostgreSQL)
- Chave do Gemini AI (já configurada)

## 🚀 Teste Local

### 1. Preparar Ambiente

```bash
# Executar script de preparação
test_local.bat
```

### 2. Iniciar Serviços

**Terminal 1 - API:**
```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd web
npm install
npm run dev
```

**Terminal 3 - Banco de Dados:**
```bash
docker-compose up postgres
```

### 3. Acessar Sistema

- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Login: `teste` / `teste123`

## 🧪 Fluxo de Teste Completo

### Teste 1: Importar Questões Reais

1. Acesse: http://localhost:3000
2. Faça login com `teste` / `teste123`
3. Clique em "🤖 IA Questões"
4. Vá na aba "📥 Importar Questões Reais"
5. Faça upload do arquivo: `data/exemplo_prova.txt`
6. Selecione disciplina: "Informática"
7. Clique em "Importar Questões"

**Resultado esperado:**
```
✅ 10 questões importadas com sucesso!
```

### Teste 2: Upload de Edital

1. Vá em "Upload Edital"
2. Crie um arquivo `edital_teste.txt` com:
```
HARDWARE
1. Componentes de hardware
2. Memória RAM e ROM
3. Processadores

REDES
1. Protocolos TCP/IP
2. Modelo OSI
3. Segurança de redes

LINUX
1. Comandos básicos
2. Gerenciamento de arquivos
3. Permissões
```
3. Faça upload do arquivo
4. Aguarde processamento

**Resultado esperado:**
```
Conteúdo programático recebido e banco de questões gerado!
```

### Teste 3: Gerar Questões com IA

1. Volte para "🤖 IA Questões"
2. Vá na aba "🤖 Gerar com IA"
3. Selecione um tópico (ex: "Hardware - Componentes de hardware")
4. Quantidade: 5
5. Dificuldade: Médio
6. Marque "Usar questões reais como referência"
7. Clique em "Gerar Questões"

**Resultado esperado:**
```
✅ 5 questões geradas com IA!
```

### Teste 4: Verificar Questões Geradas

1. Vá em "Simulados"
2. Clique em "Criar Simulado"
3. Nome: "Teste IA"
4. Questões: 5
5. Tempo: 15 minutos
6. Clique em "Criar"
7. Clique em "Iniciar"

**Resultado esperado:**
- Questões aparecem com enunciado claro
- 4 alternativas plausíveis
- Explicação detalhada após responder

## 🔍 Testes via API (Swagger)

Acesse: http://localhost:8000/docs

### 1. Importar Questões

```
POST /api/import-questions
- file: exemplo_prova.txt
- disciplina: Informática
```

### 2. Listar Tópicos

```
GET /api/topics
```

### 3. Gerar com IA

```
POST /api/generate-with-ai
Query params:
- topic_id: 1
- quantity: 5
- difficulty: MEDIO
- use_references: true
```

### 4. Listar Questões

```
GET /api/questions?limit=100
```

## 📊 Verificar Qualidade

### Estatísticas Esperadas

Após importar 10 questões e gerar 5 com IA:

```
Total de Questões: 15
Informática: 10
Hardware: 5

Por Dificuldade:
- Fácil: 3
- Médio: 8
- Difícil: 4
```

### Qualidade das Questões IA

Verifique se as questões geradas têm:

✅ Enunciado claro e objetivo
✅ 4 alternativas plausíveis
✅ Apenas 1 alternativa correta
✅ Explicação detalhada
✅ Estilo similar às questões reais
✅ Referência ao tópico do edital

## 🐛 Troubleshooting

### Erro: "GEMINI_API_KEY não configurada"

**Solução:**
```bash
# Verificar se .env existe
cat .env | grep GEMINI

# Se não existir, criar:
echo GEMINI_API_KEY=AIzaSyDVkUtP5CEkec1Du0nNA8h0ERoOsVG6g-w >> .env
```

### Erro: "No topics found"

**Solução:**
1. Faça upload de um edital primeiro
2. Aguarde processamento
3. Tente gerar novamente

### Erro: "Rate limit exceeded"

**Solução:**
- Aguarde 1 minuto
- Reduza quantidade de questões
- Gemini free tier: 60 req/min

### Questões de baixa qualidade

**Solução:**
1. Importe mais questões reais (mínimo 20)
2. Use questões da mesma disciplina
3. Ajuste dificuldade específica

## 📈 Métricas de Sucesso

### Importação
- ✅ 100% das questões válidas importadas
- ✅ Gabarito detectado corretamente
- ✅ Disciplina categorizada

### Geração IA
- ✅ 80%+ das questões aprovadas no QA
- ✅ Tempo de geração < 30s para 10 questões
- ✅ Estilo similar às questões reais

### Simulados
- ✅ Questões aparecem corretamente
- ✅ Feedback funciona
- ✅ Explicações são úteis

## 🎯 Próximos Testes

Após validar localmente:

1. **Commit e Push**
```bash
git add .
git commit -m "Test Gemini AI integration locally"
git push origin main
```

2. **Configurar no Render**
- Adicionar GEMINI_API_KEY nas variáveis de ambiente
- Aguardar redeploy

3. **Testar em Produção**
- Repetir fluxo de teste
- Verificar logs no Render
- Monitorar uso da API Gemini

## 📝 Checklist Final

Antes de fazer deploy:

- [ ] Importação de questões funciona
- [ ] Upload de edital funciona
- [ ] Geração com IA funciona
- [ ] Questões têm boa qualidade
- [ ] Simulados funcionam
- [ ] Login/logout funciona
- [ ] Navegação entre páginas funciona
- [ ] Sem erros no console
- [ ] API responde corretamente
- [ ] Banco de dados persiste dados

## 🎉 Sucesso!

Se todos os testes passaram, o sistema está pronto para produção!

**Custos estimados (Gemini):**
- 1000 questões geradas: ~$0.25
- 10000 questões: ~$2.50
- Plano gratuito: 60 req/min

**Performance:**
- Importação: ~1s para 10 questões
- Geração IA: ~3s por questão
- Total: ~30s para gerar 10 questões
