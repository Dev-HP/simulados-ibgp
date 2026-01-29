# 🤖 Guia Completo - Sistema de Geração de Questões com IA

## 📋 Visão Geral

Este sistema permite:
1. ✅ Importar questões reais de provas anteriores
2. ✅ Gerar questões novas usando Gemini AI
3. ✅ Criar simulados personalizados
4. ✅ Treino adaptativo com SRS

## 🚀 Fluxo Completo de Uso

### Passo 1: Configurar Gemini API (JÁ FEITO ✅)

A chave já está configurada:
```
GEMINI_API_KEY=[SUA_CHAVE_AQUI]
```

### Passo 2: Importar Questões Reais

1. Acesse: **🤖 IA Generator** no menu
2. Clique na aba **"📥 Importar Questões Reais"**
3. Faça upload do PDF ou TXT da prova
4. Selecione a disciplina
5. Clique em **"Importar Questões"**

**Formato do arquivo:**
```
QUESTÃO 1
Sobre hardware, é correto afirmar que:
A) RAM é memória volátil
B) ROM é memória volátil  
C) Cache é mais lenta que RAM
D) SSD é mais lento que HD
Gabarito: A

QUESTÃO 2
...
```

**Dica:** Quanto mais questões reais você importar, melhor será a qualidade das questões geradas pela IA!

### Passo 3: Upload do Edital

1. Acesse: **Upload Edital** no menu
2. Faça upload do edital do concurso (PDF ou TXT)
3. Sistema extrai automaticamente:
   - Disciplinas
   - Tópicos
   - Subtópicos

### Passo 4: Gerar Questões com IA

1. Volte para **🤖 IA Generator**
2. Clique na aba **"🤖 Gerar com IA"**
3. Selecione um tópico do edital
4. Escolha quantidade (1-50 questões)
5. Selecione dificuldade (Fácil/Médio/Difícil)
6. Clique em **"Gerar Questões"**

**O que acontece:**
- IA analisa as questões reais importadas
- Identifica padrões e estilo
- Gera questões novas no mesmo formato
- Valida qualidade automaticamente

### Passo 5: Criar Simulados

1. Acesse: **Simulados** no menu
2. Clique em **"Criar Simulado"**
3. Configure:
   - Nome do simulado
   - Número de questões
   - Tempo total
4. Sistema seleciona questões automaticamente

### Passo 6: Fazer Simulados

1. Clique em **"Iniciar"** no simulado
2. Responda as questões
3. Receba feedback imediato
4. Veja explicações detalhadas

## 📊 Estatísticas e Qualidade

### Score de Qualidade (QA)

Cada questão recebe um score de 0-100:

- **80-100**: ✅ Aprovada automaticamente
- **60-79**: ⚠️ Requer revisão
- **0-59**: ❌ Rejeitada

### Critérios de Validação

✅ Enunciado claro e objetivo
✅ 4 alternativas plausíveis
✅ Apenas 1 resposta correta
✅ Explicação detalhada
✅ Referência ao edital
✅ Sem duplicatas

## 💡 Dicas para Melhores Resultados

### 1. Importe Várias Provas
- Mínimo: 50 questões reais
- Ideal: 200+ questões reais
- Varie as bancas e anos

### 2. Organize por Disciplina
- Separe questões por tema
- Use disciplinas específicas
- Mantenha consistência

### 3. Gere em Lotes Pequenos
- 10-20 questões por vez
- Teste e ajuste
- Revise questões importantes

### 4. Use Dificuldades Variadas
- 30% Fácil
- 50% Médio
- 20% Difícil

## 🔧 Troubleshooting

### Erro: "GEMINI_API_KEY não configurada"

**Solução:**
1. Acesse Render Dashboard
2. Vá em Environment do serviço API
3. Adicione: `GEMINI_API_KEY=[SUA_CHAVE_AQUI]`
4. Salve e aguarde redeploy

### Erro: "No topics found"

**Solução:**
1. Faça upload do edital primeiro
2. Aguarde processamento
3. Tente gerar novamente

### Questões de Baixa Qualidade

**Solução:**
1. Importe mais questões reais
2. Use questões de qualidade
3. Revise manualmente questões com score < 80

### Erro: "Rate limit exceeded"

**Solução:**
1. Aguarde 1 minuto
2. Reduza quantidade de questões
3. Gere em lotes menores

## 📈 Métricas de Sucesso

### Banco de Questões Ideal

- **Mínimo**: 500 questões
- **Recomendado**: 1000+ questões
- **Cobertura**: Todos os tópicos do edital
- **Qualidade**: Score médio > 85

### Distribuição Recomendada

```
Hardware: 100 questões
Redes: 100 questões
Linux: 80 questões
Windows: 80 questões
Banco de Dados: 80 questões
Segurança: 60 questões
Outros: 100 questões
```

## 💰 Custos

### Gemini Pro - Plano Gratuito

- **Limite**: 60 requisições/minuto
- **Custo**: ~$0.00025 por questão
- **Exemplo**: 1000 questões = ~$0.25

### Estimativa Mensal

- 5000 questões/mês = ~$1.25
- 10000 questões/mês = ~$2.50
- Praticamente gratuito! 🎉

## 🎯 Casos de Uso

### Caso 1: Preparação para Concurso

1. Importe 200 questões de provas anteriores
2. Upload do edital do novo concurso
3. Gere 30 questões por tópico
4. Crie simulados semanais
5. Acompanhe evolução

### Caso 2: Treinamento Específico

1. Identifique tópicos fracos
2. Gere 50 questões do tópico
3. Faça simulados focados
4. Revise explicações
5. Repita até dominar

### Caso 3: Simulado Completo

1. Gere questões de todos os tópicos
2. Crie simulado com 60 questões
3. Configure tempo real (3h)
4. Simule prova completa
5. Analise desempenho

## 📚 Recursos Adicionais

### Documentação
- [Gemini API Docs](https://ai.google.dev/docs)
- [Google AI Studio](https://makersuite.google.com/)

### Suporte
- GitHub Issues: [Link do repositório]
- Email: [seu email]

## ✅ Checklist de Implementação

- [x] Configurar Gemini API Key
- [x] Criar interface de importação
- [x] Criar interface de geração
- [x] Implementar validação QA
- [x] Adicionar estatísticas
- [x] Documentar processo
- [ ] Importar primeiras questões reais
- [ ] Fazer upload do edital
- [ ] Gerar primeiras questões com IA
- [ ] Criar primeiro simulado
- [ ] Testar sistema completo

## 🎓 Próximos Passos

1. **Agora**: Importe suas provas reais
2. **Depois**: Faça upload do edital
3. **Em seguida**: Gere questões com IA
4. **Por fim**: Crie e faça simulados

**Boa sorte nos estudos! 🚀**
