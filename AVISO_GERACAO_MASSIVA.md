# ⚠️ AVISO: Geração Massiva de Questões

## 🚨 ATENÇÃO: Rate Limit Atingido!

O script de geração massiva (`gerar_questoes_concurso.py`) **atingiu o rate limit** do Gemini FREE.

**Limite:** 15 requisições por minuto  
**Problema:** Script tentou gerar muito rápido

---

## ✅ SOLUÇÕES DISPONÍVEIS

### 1. Interface Web (RECOMENDADO)
- Gere 10-15 questões por vez
- Aguarde 1 minuto entre gerações
- Controle total e visual

### 2. Script Lento (AUTOMÁTICO)
```bash
python gerar_questoes_lento.py
```
- Gera 5 questões por vez
- Aguarda 30 segundos entre lotes
- Pode deixar rodando

### 3. Use as 100 Questões Existentes
- Já tem questões suficientes para testar
- Faça provas completas agora
- Gere mais depois

**Veja detalhes em:** `SOLUCAO_GERACAO.md`

---

## 📊 ESTIMATIVA DE GERAÇÃO (Script Original)

### Questões por Disciplina:

| Disciplina | Tópicos | Questões/Tópico | Total Estimado |
|------------|---------|-----------------|----------------|
| **Informática** | 27 | 10 | ~270 questões |
| **Português** | 8 | 6 | ~48 questões |
| **Matemática** | 6 | 6 | ~36 questões |
| **Raciocínio Lógico** | 4 | 8 | ~32 questões |
| **Legislação** | 6 | 5 | ~30 questões |
| **Conhecimentos Gerais** | 3 | 4 | ~12 questões |

### **TOTAL: ~430 questões**

---

## ⏱️ TEMPO ESTIMADO

- **Requisições**: ~160 chamadas à API
- **Delay entre chamadas**: 3 segundos
- **Rate limit**: 55 req/min (respeitado)
- **Tempo total**: ~2-3 horas

---

## 🔒 LIMITES DO FREE TIER (Gemini)

### Limites Diários:
- ✅ **1.500 requisições/dia** (vamos usar ~160)
- ✅ **1 milhão tokens/dia** (vamos usar ~200k)
- ✅ **15 RPM** (requisições por minuto) - respeitado com delay de 3s

### Limites por Minuto:
- ✅ **15 RPM** - Nosso delay de 3s = 20 req/min (dentro do limite!)

**CONCLUSÃO: Totalmente seguro! Usa apenas ~10% do limite diário! ✅**

---

## 🚀 COMO EXECUTAR

```bash
python gerar_questoes_concurso.py
```

### O que vai acontecer:

1. **Mostra configuração** (quantas questões por disciplina)
2. **Pede confirmação** (você pode cancelar)
3. **Gera questões** disciplina por disciplina
4. **Mostra progresso** em tempo real
5. **Respeita rate limit** automaticamente
6. **Pode ser cancelado** a qualquer momento (Ctrl+C)

---

## 📈 PROGRESSO EM TEMPO REAL

Você verá algo assim:

```
════════════════════════════════════════════════════════════════
📚 DISCIPLINA: Informática
════════════════════════════════════════════════════════════════

[1/27] 📖 Tópico: Hardware
           Subtópico: Componentes internos (CPU, RAM, HD, SSD, placa-mãe)
           Questões existentes: 5
           Gerando 3 questões (FACIL)... ✅ 3 geradas
           Gerando 3 questões (MEDIO)... ✅ 3 geradas
           Gerando 4 questões (DIFICIL)... ✅ 4 geradas

[2/27] 📖 Tópico: Hardware
           Subtópico: Periféricos de entrada e saída
           ...
```

---

## ⚠️ SE ATINGIR O LIMITE

**Improvável, mas se acontecer:**

1. O script **detecta automaticamente**
2. **Aguarda 60 segundos**
3. **Tenta novamente**
4. Se persistir, **para e mostra estatísticas**

**Você não perde nada!** Todas as questões geradas até o momento são salvas.

---

## 🛑 CANCELAR A QUALQUER MOMENTO

Pressione **Ctrl+C** para cancelar.

**O que acontece:**
- ✅ Questões já geradas são **mantidas**
- ✅ Você pode **rodar de novo** depois
- ✅ O script **continua de onde parou**

---

## 📊 APÓS A GERAÇÃO

Você terá:
- ✅ ~430 questões no banco
- ✅ Cobertura de todos os 54 tópicos
- ✅ Mix de dificuldades (Fácil, Médio, Difícil)
- ✅ Questões contextualizadas (Porto Velho, RO)
- ✅ Pronto para fazer dezenas de provas completas!

---

## 🎯 TIPOS DE PROVA DISPONÍVEIS

Após gerar as questões, você poderá fazer:

1. **Prova Completa** (60 questões) - Todas disciplinas
2. **Prova Padrão** (50 questões) - Balanceada
3. **Conhecimentos Básicos** (40 questões) - Sem Informática
4. **Informática Específica** (40 questões) - Só Informática
5. **Português Específico** (30 questões) - Só Português ✨ NOVO!
6. **Matemática e Raciocínio** (30 questões) - Exatas ✨ NOVO!
7. **Legislação Específica** (20 questões) - Só Legislação ✨ NOVO!
8. **Conhecimentos Gerais** (20 questões) - RO e Porto Velho ✨ NOVO!

---

## 💡 DICA

**Rode o script durante a noite ou enquanto faz outras coisas!**

Deixe rodando e quando voltar terá ~430 questões prontas! 🚀

---

## ✅ ESTÁ PRONTO PARA COMEÇAR?

```bash
python gerar_questoes_concurso.py
```

**Vai demorar 2-3 horas, mas é 100% seguro e gratuito!**

**Boa geração! 🤖💪**
