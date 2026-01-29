# 🔒 SEGURANÇA - API KEYS

## ⚠️ NUNCA EXPONHA API KEYS NO CÓDIGO!

### ✅ O QUE FAZER:

1. **Sempre use variáveis de ambiente (.env)**
   ```python
   import os
   GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
   ```

2. **NUNCA hardcode no código**
   ```python
   # ❌ ERRADO - NUNCA FAÇA ISSO!
   GEMINI_API_KEY = "AIzaSy..."
   
   # ✅ CORRETO
   GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
   ```

3. **Verifique o .gitignore**
   ```
   .env
   .env.local
   .env.*.local
   ```

4. **Configure no Render (não no código)**
   - Dashboard → Service → Environment
   - Adicione: `GEMINI_API_KEY = [SUA_CHAVE]`

---

## 🔐 API KEY ATUAL

**Chave Gemini:**
- Configurada em: `.env` (local)
- Configurada em: Render Environment Variables (produção)
- **NUNCA** no código fonte
- **NUNCA** no GitHub

---

## 📋 CHECKLIST DE SEGURANÇA

Antes de cada commit:

- [ ] Verificar se não há API keys no código
- [ ] Confirmar que .env está no .gitignore
- [ ] Usar `os.getenv()` para todas as chaves
- [ ] Documentação usa placeholders `[SUA_CHAVE_AQUI]`

---

## 🚨 SE EXPÔS UMA CHAVE:

1. **IMEDIATAMENTE:**
   - Revogar a chave antiga no Google Cloud Console
   - Gerar nova chave
   - Atualizar .env local
   - Atualizar Render Environment Variables

2. **Limpar histórico Git (se necessário):**
   ```bash
   # Use com cuidado!
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```

3. **Verificar todos os arquivos:**
   ```bash
   grep -r "AIzaSy" .
   ```

---

## 📚 BOAS PRÁTICAS

### Para Desenvolvimento Local:
```bash
# .env (NUNCA commitar!)
GEMINI_API_KEY=sua_chave_aqui
SECRET_KEY=sua_secret_key_aqui
```

### Para Produção (Render):
- Configure via Dashboard
- Use "Environment Variables"
- Marque como "Secret" se disponível

### Para Documentação:
```markdown
GEMINI_API_KEY=[SUA_CHAVE_AQUI]
SECRET_KEY=[GERAR_NOVA_CHAVE]
```

---

## 🔗 LINKS ÚTEIS

- [Google Cloud Console](https://console.cloud.google.com/)
- [Render Environment Variables](https://render.com/docs/environment-variables)
- [LGPD - Lei Geral de Proteção de Dados](https://www.gov.br/cidadania/pt-br/acesso-a-informacao/lgpd)

---

## ✅ STATUS ATUAL

- [x] Chave antiga removida de TODOS os arquivos
- [x] Nova chave configurada no .env
- [x] .gitignore protegendo .env
- [x] Documentação usando placeholders
- [x] Código usando os.getenv()

**Sistema seguro! ✅**
