# ⚡ COMANDOS RÁPIDOS

## 🚀 Iniciar Sistema

```bash
.\iniciar_sistema.bat
```

**Aguarde até ver:**
- ✅ API: http://localhost:8000
- ✅ Frontend: http://localhost:3000

---

## 🌐 Acessar Sistema

**URL:** http://localhost:3000

**Login:**
- Usuário: `teste`
- Senha: `teste123`

---

## 🤖 Gerar Questões

### Opção 1: Interface Web (Recomendado)
1. Acessar http://localhost:3000
2. Menu: "Gerador IA"
3. Gerar 10-15 questões
4. Aguardar 1 minuto
5. Repetir

### Opção 2: Script Lento
```bash
python gerar_questoes_lento.py
```

---

## 📊 Ver Estatísticas

```bash
python -c "import sys; sys.path.insert(0, 'api'); from database import SessionLocal; from models import Question; db = SessionLocal(); print(f'Total: {db.query(Question).count()} questões'); db.close()"
```

---

## 📝 Fazer Prova

1. Acessar http://localhost:3000
2. Menu: "Prova Completa"
3. Escolher template
4. Iniciar prova

---

## 🔧 Criar Tópicos

```bash
python criar_topicos.py
```

---

## 📚 Documentação

| Arquivo | Descrição |
|---------|-----------|
| `SITUACAO_ATUAL.md` | Status do sistema |
| `SOLUCAO_GERACAO.md` | Como gerar questões |
| `GERAR_PELA_WEB.md` | Passo a passo web |
| `COMO_USAR_PROVAS.md` | Como fazer provas |
| `GUIA_COMPLETO_CONCURSO.md` | Guia completo |

---

## ⚠️ Problemas Comuns

### API não inicia
```bash
cd api
python -m uvicorn main:app --reload
```

### Frontend não inicia
```bash
cd web
npm run dev
```

### Banco de dados vazio
```bash
python criar_topicos.py
```

### Rate limit atingido
- Aguardar 1-2 minutos
- Usar interface web
- Gerar menos questões por vez

---

## 📞 Arquivos Importantes

- `simulados.db` - Banco de dados
- `.env` - Configurações (API key)
- `api/main.py` - Backend
- `web/src/App.jsx` - Frontend

---

## 🎯 Fluxo Recomendado

1. `.\iniciar_sistema.bat`
2. Abrir http://localhost:3000
3. Login: teste/teste123
4. Gerar 10 questões (Gerador IA)
5. Aguardar 1 minuto
6. Repetir até ter 100+ questões
7. Fazer prova completa
8. Revisar erros
9. Gerar mais questões nos tópicos fracos

---

**Dúvidas? Leia:** `SITUACAO_ATUAL.md`
