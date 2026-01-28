# 📚 Como Usar Provas de Referência

## 🎯 Objetivo
Usar provas de concursos de outros estados para treinar a IA Gemini e gerar questões similares para Porto Velho/RO.

## 📁 Onde Colocar as Provas

Coloque seus arquivos de provas na pasta:
```
data/provas_referencia/
```

### Formatos Aceitos:
- ✅ PDF (.pdf)
- ✅ Texto (.txt)
- ✅ Word (.docx) - será convertido para texto

## 🚀 Como Usar

### 1. Adicionar Provas de Referência

Copie suas provas para a pasta `data/provas_referencia/`:

```bash
# Exemplo de estrutura:
data/provas_referencia/
  ├── prova_sp_tecnico_informatica_2023.pdf
  ├── prova_mg_analista_ti_2022.pdf
  ├── prova_pr_tecnico_2024.txt
  └── ...
```

**Seus arquivos já copiados:**
- ✅ `gabarito_definitivo.pdf`
- ✅ `ibgp_sao_joao_del_rei_mg_2021.pdf`

### 2. Importar Questões Automaticamente

**Opção A - Script Automático (Recomendado):**

```bash
# Execute o script de importação:
.\importar_provas.bat
```

O script vai:
- ✅ Verificar se a API está rodando
- ✅ Fazer login automaticamente
- ✅ Importar todos os PDFs da pasta
- ✅ Mostrar estatísticas de importação

**Opção B - Interface Web:**

1. Acesse: http://localhost:3000
2. Faça login (usuário: `teste`, senha: `teste123`)
3. Vá em **"Gerador IA"**
4. Clique em **"Importar de Arquivo"**
5. Selecione o arquivo da prova
6. O sistema vai:
   - Extrair as questões automaticamente
   - Identificar alternativas e gabaritos
   - Salvar no banco de dados

### 3. Gerar Novas Questões com IA

Depois de importar algumas provas:

1. Vá em **"Gerador IA"**
2. Escolha o tema (ex: "Redes de Computadores")
3. Defina quantidade (ex: 10 questões)
4. Clique em **"Gerar com IA"**

A IA Gemini vai:
- Analisar as questões importadas
- Aprender o estilo e dificuldade
- Gerar questões novas e similares
- Adaptar para o contexto de Porto Velho/RO

## 📊 Estatísticas e Controle

### Limites da API Gemini (Free Tier):
- ⏱️ **55 requisições por minuto**
- 📅 **1.400 requisições por dia**

O sistema controla automaticamente e mostra:
- Requisições usadas hoje
- Requisições restantes
- Tempo até reset

## 💡 Dicas

### Para Melhores Resultados:

1. **Quantidade**: Importe pelo menos 5-10 provas diferentes
2. **Variedade**: Use provas de diferentes estados e anos
3. **Qualidade**: Prefira provas completas com gabarito
4. **Temas**: Organize por assunto (Redes, Segurança, Programação, etc.)

### Exemplo de Uso:

```
1. Importar 10 provas de SP, MG, PR sobre "Redes"
2. Gerar 20 questões novas sobre "Redes" para Porto Velho
3. Criar simulado com essas questões
4. Estudantes fazem o simulado
5. Sistema analisa desempenho e gera mais questões nos pontos fracos
```

## 🔧 Comandos Úteis

### Verificar Provas Importadas:
```bash
# Via API
curl http://localhost:8000/api/questions/stats
```

### Limpar Cache da IA:
```bash
# Via API
curl -X POST http://localhost:8000/api/ai/clear-cache
```

## ⚠️ Importante

- As provas de referência **NÃO** são copiadas diretamente
- A IA **aprende o estilo** e **gera questões originais**
- Todas as questões geradas são **únicas e inéditas**
- O sistema respeita direitos autorais

## 📞 Suporte

Se tiver dúvidas:
1. Veja `TESTE_GEMINI.md` para detalhes técnicos
2. Veja `docs/GEMINI_SETUP.md` para configuração
3. Veja `COMO_TESTAR.md` para testes

---

**Pronto para começar!** 🚀

Coloque suas provas em `data/provas_referencia/` e comece a gerar questões!
