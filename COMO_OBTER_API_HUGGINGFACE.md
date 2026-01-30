# 🔑 COMO OBTER API KEY DO HUGGINGFACE

## 📋 PASSO A PASSO COMPLETO

### **1️⃣ ACESSAR O SITE**
🔗 **Vá para**: https://huggingface.co

### **2️⃣ CRIAR CONTA (se não tiver)**
- Clique em **"Sign Up"** no canto superior direito
- Preencha:
  - **Email**: seu email
  - **Username**: escolha um nome de usuário
  - **Password**: senha segura
- Confirme o email

### **3️⃣ FAZER LOGIN**
- Clique em **"Sign In"**
- Digite email e senha
- Entre na sua conta

### **4️⃣ ACESSAR CONFIGURAÇÕES**
🔗 **Vá diretamente para**: https://huggingface.co/settings/tokens

**OU:**
1. Clique no seu **avatar** (foto de perfil) no canto superior direito
2. Clique em **"Settings"**
3. No menu lateral, clique em **"Access Tokens"**

### **5️⃣ CRIAR NOVA API KEY**
1. Clique no botão **"New token"**
2. Preencha:
   - **Name**: `simulados-ibgp` (ou qualquer nome)
   - **Role**: Selecione **"Read"** (suficiente para usar modelos)
3. Clique em **"Generate a token"**

### **6️⃣ COPIAR A CHAVE**
- ⚠️ **IMPORTANTE**: A chave aparece **apenas uma vez**!
- Copie a chave que começa com `hf_`
- Exemplo: `hf_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890`

---

## 🔧 CONFIGURAR NO PROJETO

### **OPÇÃO 1: Arquivo .env (Local)**
```bash
# Abra o arquivo .env e adicione:
HUGGINGFACE_API_KEY=hf_sua_chave_aqui
```

### **OPÇÃO 2: Render (Produção)**
1. Acesse seu projeto no Render
2. Vá em **Environment**
3. Adicione nova variável:
   - **Key**: `HUGGINGFACE_API_KEY`
   - **Value**: `hf_sua_chave_aqui`
4. Clique **Save**

---

## ✅ TESTAR A CHAVE

Execute o teste:
```bash
python testar_huggingface.py
```

Se aparecer:
```
✅ API Key configurada: hf_xxxxxxxxxx...
✅ Conexão bem-sucedida
```

**Sua chave está funcionando!** 🎉

---

## 💰 LIMITES GRATUITOS

### **TIER GRATUITO:**
- **$0.10/mês** de créditos gratuitos
- **Suficiente para**: ~100-200 questões/mês
- **Rate limiting**: Generoso (sem problemas)

### **SE PRECISAR DE MAIS:**
- **Pro Plan**: $9/mês
- **Inclui**: $2/mês de créditos + pay-as-you-go
- **Muito barato**: ~$0.001 por questão

---

## 🚨 DICAS IMPORTANTES

### **✅ FAÇA:**
- Guarde a chave em local seguro
- Use apenas em variáveis de ambiente
- Teste antes de usar em produção

### **❌ NÃO FAÇA:**
- Não compartilhe a chave
- Não coloque no código fonte
- Não commite no GitHub

---

## 🔄 SE DER PROBLEMA

### **Erro: "Invalid token"**
1. Verifique se copiou a chave completa
2. Certifique-se que começa com `hf_`
3. Gere uma nova chave se necessário

### **Erro: "Model loading"**
- É normal! Modelos demoram ~30s para carregar
- O sistema tem retry automático

### **Erro: "Rate limit"**
- Aguarde alguns minutos
- Sistema tem fallback automático

---

## 🎯 RESUMO RÁPIDO

1. **Acesse**: https://huggingface.co/settings/tokens
2. **Crie conta** se não tiver
3. **Clique**: "New token"
4. **Nome**: `simulados-ibgp`
5. **Role**: "Read"
6. **Copie** a chave `hf_...`
7. **Configure** no .env ou Render
8. **Teste** com `python testar_huggingface.py`

**Pronto! Sistema híbrido funcionando!** 🚀