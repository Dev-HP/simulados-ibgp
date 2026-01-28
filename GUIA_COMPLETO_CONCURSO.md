# 🎯 Guia Completo - Sistema de Preparação para Concurso

## Câmara Municipal de Porto Velho/RO - Técnico em Informática

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Iniciar o Sistema](#iniciar-o-sistema)
3. [Funcionalidades Principais](#funcionalidades-principais)
4. [Gerar Questões com IA](#gerar-questões-com-ia)
5. [Fazer Provas Completas](#fazer-provas-completas)
6. [Dicas de Estudo](#dicas-de-estudo)
7. [Conteúdo Programático](#conteúdo-programático)

---

## 🎓 Visão Geral

Este sistema foi desenvolvido especificamente para você se preparar para o concurso de **Técnico em Informática** da Câmara Municipal de Porto Velho/RO.

### ✨ Recursos Principais:

- 🤖 **Geração de Questões com IA** (Google Gemini)
- 📝 **Provas Completas** simulando o concurso real
- 📊 **Estatísticas Detalhadas** do seu progresso
- 🎯 **54 Tópicos** organizados por disciplina
- ⏱️ **Simulação com Tempo** igual à prova real
- 📚 **Banco de Questões** em constante crescimento

---

## 🚀 Iniciar o Sistema

### Passo 1: Iniciar API e Frontend

```bash
# Execute o script de inicialização
.\iniciar_sistema.bat
```

Isso vai:
- ✅ Iniciar a API na porta 8000
- ✅ Iniciar o Frontend na porta 3000
- ✅ Abrir o navegador automaticamente

### Passo 2: Fazer Login

- **Usuário:** `teste`
- **Senha:** `teste123`

---

## 🎯 Funcionalidades Principais

### 1. 🏠 Dashboard

O Dashboard é sua central de comando:

- **Estatísticas Rápidas**: Veja quantas questões estão disponíveis
- **Acesso Rápido**: Links para todas as funcionalidades
- **Dicas de Estudo**: Orientações para sua preparação

### 2. 🎯 Prova Completa (RECOMENDADO!)

A funcionalidade mais importante do sistema:

**Tipos de Prova Disponíveis:**

1. **Técnico em Informática - Completo** (60 questões)
   - 30 Informática
   - 10 Português
   - 8 Matemática
   - 7 Raciocínio Lógico
   - 5 Legislação

2. **Técnico em Informática - Padrão** (50 questões)
   - 25 Informática
   - 10 Português
   - 8 Matemática
   - 5 Raciocínio Lógico
   - 2 Legislação

3. **Conhecimentos Básicos** (40 questões)
   - Sem Informática
   - Foco em Português, Matemática e Raciocínio Lógico

4. **Informática Específica** (40 questões)
   - 100% Informática

**Recursos da Prova:**
- ⏱️ **Timer** com contagem regressiva
- 🗺️ **Mapa de Questões** para navegação rápida
- 🚩 **Marcar Questões** para revisar depois
- 📊 **Estatísticas** ao finalizar

### 3. 🤖 Gerar com IA

Crie questões personalizadas sobre qualquer tópico:

**Como usar:**
1. Selecione a **disciplina**
2. Escolha o **tópico**
3. Defina a **quantidade** (1-20 questões)
4. Selecione a **dificuldade** (Fácil, Médio, Difícil)
5. Clique em **Gerar**

**Dica:** Use referências de provas anteriores para questões mais realistas!

### 4. 📚 Questões

Pratique questões individuais por:
- Disciplina
- Tópico
- Dificuldade

---

## 🤖 Gerar Questões com IA

### Geração Manual (Interface Web)

1. Acesse **"Gerar com IA"** no menu
2. Configure os parâmetros
3. Clique em **Gerar**
4. Aguarde (leva ~10-30 segundos)

### Geração Massiva (Script Python)

Para gerar centenas de questões automaticamente:

```bash
python gerar_questoes_concurso.py
```

**O que o script faz:**
- ✅ Gera questões para TODOS os 54 tópicos
- ✅ Distribui por dificuldade (Fácil, Médio, Difícil)
- ✅ Respeita o rate limit da API do Gemini
- ✅ Foca mais em Informática (50% das questões)
- ✅ Mostra progresso em tempo real

**Estimativa:**
- ~500-800 questões geradas
- Tempo: 2-4 horas
- Custo: GRÁTIS (dentro do free tier do Gemini)

---

## 📝 Fazer Provas Completas

### Passo a Passo:

1. **Acesse "Prova Completa"** no Dashboard
2. **Escolha o tipo de prova** (recomendo começar com "Padrão")
3. **Clique em "Iniciar Prova"**
4. **Responda as questões:**
   - Use o **mapa de questões** para navegar
   - **Marque** questões difíceis para revisar
   - Fique de olho no **timer**
5. **Finalize** quando terminar ou quando o tempo acabar
6. **Veja suas estatísticas**

### Dicas Durante a Prova:

- ⏱️ **Gerencie seu tempo**: ~1.5 minutos por questão
- 🎯 **Responda as fáceis primeiro**: Garanta pontos
- 🚩 **Marque as difíceis**: Volte depois se sobrar tempo
- 🧘 **Mantenha a calma**: É só um treino!

---

## 💡 Dicas de Estudo

### Estratégia de Preparação:

#### Semana 1-2: Diagnóstico
- ✅ Faça uma **prova completa** sem estudar
- ✅ Identifique seus **pontos fracos**
- ✅ Foque 70% do tempo em **Informática**

#### Semana 3-6: Estudo Focado
- ✅ Estude **2-3 tópicos por dia**
- ✅ Gere **10-20 questões** de cada tópico
- ✅ Revise **erros** imediatamente
- ✅ Faça **1 prova completa** por semana

#### Semana 7-8: Revisão Intensiva
- ✅ Faça **1 prova completa** por dia
- ✅ Revise **todos os tópicos** rapidamente
- ✅ Foque em **legislação de RO**
- ✅ Pratique **interpretação de texto**

### Distribuição de Tempo de Estudo:

```
📊 Sugestão de Distribuição:

50% - Informática (conhecimento específico)
20% - Português (interpretação + gramática)
15% - Matemática + Raciocínio Lógico
10% - Legislação (leis de RO + federais)
5%  - Conhecimentos Gerais (atualidades)
```

### Cronograma Diário Ideal:

```
🌅 Manhã (2h):
  - 1h: Estudo teórico (vídeos, apostilas)
  - 1h: Questões do tópico estudado

🌆 Tarde (2h):
  - 1h: Revisão de erros
  - 1h: Prova completa (3x por semana)

🌙 Noite (1h):
  - Revisão rápida
  - Flashcards
  - Descanso mental
```

---

## 📚 Conteúdo Programático

### 💻 INFORMÁTICA (27 tópicos - 50% da prova)

#### Hardware (5 tópicos)
- Componentes internos (CPU, RAM, HD, SSD, placa-mãe)
- Periféricos de entrada e saída
- Barramentos e interfaces (USB, SATA, PCI)
- Fontes de alimentação e refrigeração
- Manutenção preventiva e corretiva

#### Redes (6 tópicos)
- Modelo OSI e TCP/IP
- Protocolos (HTTP, HTTPS, FTP, SMTP, DNS, DHCP)
- Endereçamento IP (IPv4 e IPv6)
- Topologias de rede
- Equipamentos (switch, roteador, hub, modem)
- Cabeamento estruturado

#### Sistemas Operacionais (5 tópicos)
- Windows 10/11 (instalação e configuração)
- Gerenciamento de arquivos e pastas
- Linux (comandos básicos)
- Gerenciamento de usuários e permissões
- Processos e memória

#### Segurança (4 tópicos)
- Backup e recuperação
- Antivírus e antimalware
- Firewall e criptografia
- Políticas de segurança

#### Aplicativos (4 tópicos)
- Microsoft Office (Word, Excel, PowerPoint)
- LibreOffice

#### Internet e Banco de Dados (3 tópicos)
- Navegadores e e-mail
- SQL básico

### 📖 PORTUGUÊS (8 tópicos - 20% da prova)
- Interpretação de Texto
- Ortografia
- Acentuação Gráfica
- Pontuação
- Concordância (verbal e nominal)
- Regência
- Crase
- Redação Oficial

### 🔢 MATEMÁTICA (6 tópicos - 15% da prova)
- Operações Fundamentais
- Frações e Decimais
- Porcentagem
- Regra de Três
- Equações
- Geometria Básica

### 🧩 RACIOCÍNIO LÓGICO (4 tópicos - 10% da prova)
- Sequências Lógicas
- Proposições Lógicas
- Diagramas de Venn
- Problemas Lógicos

### 🏛️ LEGISLAÇÃO (6 tópicos - 10% da prova)
- Constituição Federal
- Lei 8.112/90 (Servidores Públicos)
- Estatuto dos Servidores de Rondônia
- Ética no Serviço Público
- Lei de Licitações (14.133/2021)
- Lei de Acesso à Informação

### 🌍 CONHECIMENTOS GERAIS (3 tópicos - 5% da prova)
- Atualidades
- Rondônia (geografia, história, economia)
- Porto Velho (história, cultura)

---

## 🎯 Metas de Questões

### Objetivo Mínimo:
- ✅ 500 questões no banco
- ✅ 10 provas completas realizadas
- ✅ 80% de acerto em Informática

### Objetivo Ideal:
- ✅ 1000+ questões no banco
- ✅ 20+ provas completas realizadas
- ✅ 85%+ de acerto geral

---

## 🆘 Solução de Problemas

### API não inicia:
```bash
# Verificar se a porta 8000 está livre
netstat -ano | findstr :8000

# Reiniciar o sistema
.\iniciar_sistema.bat
```

### Frontend não carrega:
```bash
# Limpar cache do navegador
Ctrl + Shift + Delete

# Ou acessar diretamente
http://localhost:3000
```

### Erro ao gerar questões:
- ✅ Verifique se a chave do Gemini está no `.env`
- ✅ Verifique se não atingiu o rate limit (55 req/min)
- ✅ Aguarde 1 minuto e tente novamente

---

## 📞 Suporte

Se tiver problemas:
1. Verifique o arquivo `COMO_TESTAR.md`
2. Leia o `INICIO_RAPIDO.md`
3. Execute `.\start_and_test.bat` para diagnóstico

---

## 🎉 Boa Sorte!

Você tem todas as ferramentas necessárias para passar no concurso!

**Lembre-se:**
- 📚 Consistência > Intensidade
- 🎯 Qualidade > Quantidade
- 💪 Prática > Teoria
- 🧘 Calma > Ansiedade

**Você consegue! 🚀**

---

*Sistema desenvolvido com ❤️ para sua aprovação*
