# 🚀 Início Rápido - Testar Sistema em 3 Passos

## Opção 1: Automático (Recomendado)

Execute um único script que faz tudo:

```bash
start_and_test.bat
```

Isso vai:
1. ✅ Verificar dependências
2. ✅ Iniciar banco de dados
3. ✅ Iniciar API
4. ✅ Executar todos os testes
5. ✅ Gerar relatório

---

## Opção 2: Manual (3 Terminais)

### Terminal 1: Banco de Dados

```bash
docker-compose up postgres
```

Se não tiver Docker, pule este passo (vai usar SQLite).

### Terminal 2: API

```bash
cd api
uvicorn main:app --reload
```

Aguarde ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Terminal 3: Testes

```bash
python run_all_tests.py
```

---

## Opção 3: Apenas API (Sem Testes)

Se só quer ver o sistema funcionando:

```bash
# Terminal 1 - API
cd api
uvicorn main:app --reload

# Terminal 2 - Frontend
cd web
npm run dev
```

Acesse: http://localhost:3000

---

## ✅ Resultado Esperado

Se tudo estiver OK, você verá:

```
🎉 TODOS OS TESTES PASSARAM!
   Sistema está funcionando perfeitamente!

Relatório salvo em: test_report_YYYYMMDD_HHMMSS.txt
```

---

## 🆘 Problemas?

### "Python não encontrado"
```bash
# Instalar Python 3.11+
# https://www.python.org/downloads/
```

### "Module 'requests' not found"
```bash
pip install requests
```

### "API não está rodando"
```bash
# Abrir novo terminal e executar:
cd api
uvicorn main:app --reload
```

### "Port 8000 already in use"
```bash
# Parar processo na porta 8000
taskkill /F /IM python.exe

# Ou usar outra porta
uvicorn main:app --reload --port 8001
```

---

## 📊 O Que os Testes Verificam

- ✅ API está funcionando
- ✅ Login funciona
- ✅ Importar questões funciona
- ✅ Gerar questões com IA funciona
- ✅ Criar simulados funciona
- ✅ Rate limiting protege a API
- ✅ Banco de dados persiste dados

---

## 🎯 Próximo Passo

Depois que os testes passarem localmente:

1. Fazer commit e push
2. Configurar GEMINI_API_KEY no Render
3. Aguardar deploy
4. Testar em produção

---

## 📚 Mais Informações

- **COMO_TESTAR.md** - Guia completo de testes
- **TESTE_AUTOMATIZADO.md** - 36 tasks detalhadas
- **docs/RATE_LIMITING.md** - Sobre rate limiting
