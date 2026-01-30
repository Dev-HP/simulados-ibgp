# ⚡ Quick Start

## 🎯 Para começar AGORA

### 1. Testar o sistema em produção

```bash
python test_final.py
```

### 2. Configurar API Key no Render

1. Acesse: https://dashboard.render.com
2. Selecione: `simulados-ibgp`
3. Vá em: **Environment**
4. Adicione:
   ```
   HUGGINGFACE_API_KEY=sua_chave_aqui
   ```
5. Salve e aguarde redeploy (5-10 min)

### 3. Testar novamente

```bash
python test_final.py
```

Se aparecer "✅ SISTEMA FUNCIONANDO!" → Pronto!

## 🔧 Desenvolvimento Local

### Backend

```bash
cd api
pip install -r requirements.txt
uvicorn main:app --reload
```

Acesse: http://localhost:8000/docs

### Frontend

```bash
cd web
npm install
npm run dev
```

Acesse: http://localhost:5173

## 📊 Gerar Questões

### Via API

```bash
curl -X POST "http://localhost:8000/api/generate-with-ai" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "topic_id": 1,
    "quantity": 10,
    "strategy": "huggingface_only"
  }'
```

### Via Script

```bash
python scripts/database/gerar_prova_60_questoes.py
```

## 🗄️ Popular Banco

```bash
# Criar tópicos
python scripts/database/criar_topicos.py

# Popular questões
python scripts/database/popular_banco_producao.py
```

## 🚀 Deploy

```bash
# Commit e push (deploy automático)
git add .
git commit -m "Update"
git push origin main
```

## 📝 Estrutura Importante

```
api/                    # Backend
web/                    # Frontend
scripts/                # Scripts úteis
  ├── deploy/          # Deploy
  ├── database/        # Banco de dados
  └── tests/           # Testes
test_final.py          # Teste principal
.env                   # Configurações locais
```

## ❓ Problemas?

1. Verifique logs: https://dashboard.render.com
2. Execute: `python test_final.py`
3. Veja: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
