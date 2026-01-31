# 📚 COMO USAR O SISTEMA DE SIMULADOS

## 🚀 Acesso Rápido

**Frontend:** https://simulados-ibgp-1.onrender.com  
**Backend:** https://simulados-ibgp.onrender.com  
**Login:** `teste` / `teste123`

---

## 📝 PASSO A PASSO

### 1. Acessar o Sistema

1. Abra seu navegador
2. Acesse: https://simulados-ibgp-1.onrender.com
3. Você verá a tela de login

### 2. Fazer Login

1. Digite o usuário: `teste`
2. Digite a senha: `teste123`
3. Clique em "Entrar"

### 3. Gerar uma Prova Completa

#### Opção A: Pelo Frontend
1. Após o login, clique em "Prova Completa" no menu
2. Clique em "Gerar Nova Prova"
3. O sistema irá gerar uma prova com 60 questões seguindo o edital:
   - 30 questões de Informática (50%)
   - 9 questões de Português (15%)
   - 6 questões de Matemática (10%)
   - 4 questões de Raciocínio Lógico (7%)
   - 7 questões de Legislação (11%)
   - 4 questões de Conhecimentos Gerais (7%)

#### Opção B: Pela API
```bash
# Gerar prova
curl -X POST https://simulados-ibgp.onrender.com/api/prova-completa/gerar \
  -H "Authorization: Bearer SEU_TOKEN"

# Listar provas
curl https://simulados-ibgp.onrender.com/api/prova-completa \
  -H "Authorization: Bearer SEU_TOKEN"
```

### 4. Fazer a Prova

1. Clique na prova gerada
2. Leia cada questão com atenção
3. Selecione a alternativa que você acha correta
4. Clique em "Próxima" para avançar
5. Ao final, clique em "Finalizar Prova"

### 5. Ver Resultado

1. Após finalizar, você verá:
   - Nota final (0-100)
   - Acertos por disciplina
   - Tempo gasto
   - Questões que errou (com explicação)

---

## 🎯 FUNCIONALIDADES

### Banco de Questões
- **160 questões** disponíveis
- Todas as disciplinas do edital
- Questões geradas por IA (HuggingFace)
- Explicações detalhadas

### Provas Personalizadas
- Gere quantas provas quiser
- Cada prova é única (questões aleatórias)
- Segue exatamente o edital IBGP

### Estatísticas
- Acompanhe seu desempenho
- Veja quais disciplinas precisa melhorar
- Histórico de provas realizadas

---

## 📊 ENDPOINTS DA API

### Autenticação
```bash
# Login
POST /api/token
Body: username=teste&password=teste123
```

### Questões
```bash
# Listar todas
GET /api/questions

# Filtrar por disciplina
GET /api/questions?disciplina=Informática

# Buscar uma questão
GET /api/questions/{id}
```

### Prova Completa
```bash
# Gerar prova
POST /api/prova-completa/gerar

# Listar provas
GET /api/prova-completa

# Buscar prova específica
GET /api/prova-completa/{id}

# Submeter respostas
POST /api/prova-completa/{id}/submit
Body: {"respostas": {"1": "A", "2": "B", ...}}
```

### Tópicos
```bash
# Listar todos
GET /api/topics

# Filtrar por disciplina
GET /api/topics?disciplina=Informática
```

---

## 🔧 TROUBLESHOOTING

### Problema: Não consigo fazer login
**Solução:**
1. Verifique se está usando: `teste` / `teste123`
2. Limpe o cache do navegador
3. Tente em modo anônimo

### Problema: Erro de CORS
**Solução:**
1. O CORS já está configurado
2. Aguarde alguns segundos e tente novamente
3. Limpe o cache do navegador

### Problema: Prova não carrega
**Solução:**
1. Verifique sua conexão com a internet
2. Recarregue a página (F5)
3. Faça logout e login novamente

### Problema: Questões não aparecem
**Solução:**
1. Verifique se há questões no banco:
   ```bash
   python check_questions.py
   ```
2. Se necessário, gere mais questões:
   ```bash
   python generate_missing_questions.py
   ```

---

## 💡 DICAS DE USO

### Para Estudar
1. **Faça múltiplas provas:** Você tem 160 questões, pode fazer várias provas diferentes
2. **Revise os erros:** Leia as explicações das questões que errou
3. **Foque nas fraquezas:** Veja quais disciplinas você erra mais
4. **Simule o tempo real:** A prova real tem 3 horas (180 minutos)

### Para Praticar
1. **Comece com provas parciais:** Faça provas de uma disciplina só
2. **Aumente a dificuldade:** Depois faça provas completas
3. **Cronometre-se:** Tente fazer em menos de 3 horas
4. **Revise sempre:** Não pule as explicações

### Para o Dia da Prova
1. **Descanse bem:** Durma cedo na véspera
2. **Chegue cedo:** Evite atrasos
3. **Leia com atenção:** Não tenha pressa
4. **Confie no seu preparo:** Você estudou!

---

## 📞 SUPORTE

### Verificar Status do Sistema
```bash
python test_complete_system.py
```

### Verificar Questões
```bash
python check_questions.py
```

### Ver Resumo Final
```bash
cat RESUMO_FINAL.md
```

### Documentação da API
Acesse: https://simulados-ibgp.onrender.com/docs

---

## 🎓 SOBRE O CONCURSO

**Cargo:** Técnico em Informática  
**Órgão:** Câmara Municipal de Porto Velho/RO  
**Banca:** IBGP  
**Questões:** 60 (múltipla escolha)  
**Tempo:** 3 horas  

### Distribuição das Questões
- Informática: 30 questões (50%)
- Português: 9 questões (15%)
- Matemática: 6 questões (10%)
- Raciocínio Lógico: 4 questões (7%)
- Legislação: 7 questões (11%)
- Conhecimentos Gerais: 4 questões (7%)

---

## ✨ RECURSOS DISPONÍVEIS

- ✅ 160 questões geradas por IA
- ✅ Todas as disciplinas do edital
- ✅ Explicações detalhadas
- ✅ Provas ilimitadas
- ✅ Estatísticas de desempenho
- ✅ Interface amigável
- ✅ Acesso via web (qualquer dispositivo)
- ✅ Banco PostgreSQL (persistente)

---

## 🎯 BOA SORTE!

Você tem tudo que precisa para se preparar bem!

- 160 questões para praticar
- Sistema completo e funcional
- Provas ilimitadas
- Explicações detalhadas

**Estude com dedicação e confie no seu preparo! 🍀**

---

*Última atualização: 31/01/2026*  
*Sistema: Simulados IBGP v1.0*
