# 🤖 Configuração do Gemini AI para Geração de Questões

Este guia explica como configurar e usar o Gemini Pro para gerar questões realistas baseadas em provas reais.

## 📋 Pré-requisitos

1. Conta no Google AI Studio
2. Chave de API do Gemini
3. Provas reais em PDF ou TXT

## 🔑 Obter Chave da API Gemini

1. Acesse: https://makersuite.google.com/app/apikey
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada

## ⚙️ Configuração

### 1. Adicionar chave no arquivo .env

```bash
GEMINI_API_KEY=sua_chave_aqui
```

### 2. No Render (Produção)

1. Acesse o dashboard do Render
2. Vá em "Environment" do serviço da API
3. Adicione a variável:
   - Key: `GEMINI_API_KEY`
   - Value: sua chave do Gemini

## 📚 Como Usar

### 1. Importar Questões Reais

Primeiro, importe questões de provas reais para servir como referência:

```bash
# Via interface web
POST /api/import-questions
- Faça upload do PDF ou TXT da prova
- Especifique a disciplina (ex: "Informática")

# Formato esperado do arquivo:
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

### 2. Gerar Questões com IA

Depois de ter questões reais importadas:

```bash
POST /api/generate-with-ai
{
  "topic_id": 1,
  "quantity": 10,
  "difficulty": "MEDIO",
  "use_references": true
}
```

**Parâmetros:**
- `topic_id`: ID do tópico do edital
- `quantity`: Quantas questões gerar (1-50)
- `difficulty`: FACIL, MEDIO ou DIFICIL (opcional)
- `use_references`: true para usar questões reais como referência

### 3. Melhorar Questões Existentes

```bash
POST /api/improve-question/123
```

Melhora uma questão específica usando IA.

## 🎯 Fluxo Completo Recomendado

### Passo 1: Importar Provas Reais
```
1. Acesse: Upload Edital
2. Faça upload das provas reais (PDF/TXT)
3. Sistema importa e categoriza automaticamente
```

### Passo 2: Upload do Edital
```
1. Faça upload do edital do concurso
2. Sistema extrai tópicos automaticamente
```

### Passo 3: Gerar Banco com IA
```
1. Para cada tópico, gere questões com IA
2. Sistema usa as questões reais como referência
3. Gemini cria questões novas no mesmo estilo
```

## 📊 Qualidade das Questões

O sistema garante qualidade através de:

✅ **Validação QA Automática**
- Verifica clareza do enunciado
- Valida alternativas plausíveis
- Checa explicação adequada

✅ **Baseado em Questões Reais**
- Usa provas anteriores como referência
- Mantém estilo e dificuldade similares

✅ **Revisão Manual**
- Questões marcadas para revisão quando necessário
- Score de qualidade (0-100)

## 💰 Custos

O Gemini Pro tem um plano gratuito generoso:

- **Gratuito**: 60 requisições/minuto
- **Custo**: ~$0.00025 por questão gerada
- **Exemplo**: 1000 questões = ~$0.25

## 🔧 Troubleshooting

### Erro: "GEMINI_API_KEY não configurada"
- Verifique se adicionou a chave no .env
- Reinicie o servidor da API

### Erro: "Rate limit exceeded"
- Aguarde 1 minuto
- Reduza a quantidade de questões por requisição

### Questões de baixa qualidade
- Importe mais questões reais como referência
- Ajuste o prompt no código (gemini_generator.py)
- Use difficulty específica

## 📝 Exemplo de Uso Completo

```python
# 1. Importar 50 questões reais
POST /api/import-questions
File: prova_tecnico_2023.pdf
Disciplina: Informática

# 2. Gerar 30 questões novas sobre Hardware
POST /api/generate-with-ai
{
  "topic_id": 5,  # Hardware
  "quantity": 30,
  "difficulty": "MEDIO",
  "use_references": true
}

# 3. Melhorar questões com score baixo
POST /api/improve-question/123
POST /api/improve-question/124
```

## 🎓 Dicas

1. **Importe várias provas** - Quanto mais referências, melhor
2. **Varie as dificuldades** - Gere questões fáceis, médias e difíceis
3. **Revise manualmente** - Sempre revise questões importantes
4. **Use tópicos específicos** - Gere por tópico, não tudo de uma vez
5. **Monitore o score QA** - Questões com score < 80 precisam revisão

## 📚 Recursos

- [Documentação Gemini](https://ai.google.dev/docs)
- [Google AI Studio](https://makersuite.google.com/)
- [Pricing](https://ai.google.dev/pricing)
