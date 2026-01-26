# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-01-26

### Adicionado
- Sistema completo de simulados adaptativos
- Ingestão automática de editais (TXT/PDF)
- Parse hierárquico de conteúdo programático
- Geração automática de questões no estilo IBGP
- Validação QA de questões
- Simulados configuráveis (oficiais e customizados)
- Feedback imediato com explicações detalhadas
- Treino adaptativo com algoritmo SRS
- Métricas e analytics por usuário
- Export em múltiplos formatos (GIFT, CSV, JSON)
- API REST completa com OpenAPI/Swagger
- Frontend React com interface intuitiva
- Autenticação JWT
- Containerização com Docker
- CI/CD com GitHub Actions
- Documentação completa
- Testes automatizados
- Scripts de seed e validação

### Funcionalidades Principais
- ✅ Upload e parse de editais
- ✅ Geração de 30+ questões por tópico amplo
- ✅ Questões no estilo IBGP com distratores realistas
- ✅ Simulados espelhando provas oficiais
- ✅ Relatórios detalhados com plano de estudo
- ✅ Priorização de tópicos fracos (<60% acerto)
- ✅ Espaçamento de revisão (SRS)
- ✅ Questões similares para reforço
- ✅ Classificação de erros (conceitual, cálculo, leitura)

### Conteúdo Programático Coberto
- Hardware e componentes
- Algoritmos e estruturas de dados
- Banco de dados (SQL, modelagem ER)
- Sistemas operacionais (Linux, Windows)
- Redes (TCP/IP, protocolos, VLAN)
- Segurança da informação
- Noções de Informática (Excel, atalhos)
- Legislação (LGPD, Marco Civil)

### Tecnologias
- Backend: FastAPI (Python 3.11)
- Frontend: React 18 + Vite
- Database: PostgreSQL 15
- Cache: Redis 7
- Proxy: Nginx
- CI/CD: GitHub Actions
- Containerização: Docker + Docker Compose

## [Unreleased]

### Planejado
- Rate limiting
- Websockets para simulados em tempo real
- PWA (Progressive Web App)
- OAuth2 com mais provedores
- Gamificação avançada
- Machine Learning para geração de questões
- Análise preditiva de desempenho
- Suporte a mais bancas (além de IBGP)
