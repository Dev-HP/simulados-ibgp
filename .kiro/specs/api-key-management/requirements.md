# Requirements Document

## Introduction

Sistema de gerenciamento de API keys do Gemini para geração de questões, com fallback automático entre modelos e recuperação de quota.

## Glossary

- **Gemini_API**: Serviço de IA do Google para geração de conteúdo
- **Rate_Limiter**: Sistema de controle de requisições por minuto/dia
- **Flash_Lite**: Modelo Gemini com menor consumo de quota
- **Quota_Manager**: Sistema de monitoramento e recuperação de quota

## Requirements

### Requirement 1: Gerenciamento de API Key

**User Story:** Como desenvolvedor, eu quero que o sistema gerencie automaticamente as API keys do Gemini, para que a geração de questões funcione sem interrupção.

#### Acceptance Criteria

1. WHEN uma API key é configurada, THE System SHALL validar sua autenticidade antes de usar
2. WHEN uma API key expira ou é inválida, THE System SHALL reportar o erro claramente
3. WHEN múltiplas API keys estão disponíveis, THE System SHALL fazer fallback automático
4. THE System SHALL armazenar API keys apenas em variáveis de ambiente seguras

### Requirement 2: Fallback entre Modelos Gemini

**User Story:** Como usuário, eu quero que o sistema tente diferentes modelos do Gemini automaticamente, para maximizar as chances de geração bem-sucedida.

#### Acceptance Criteria

1. WHEN gemini-2.5-pro falha por quota, THE System SHALL tentar gemini-2.5-flash
2. WHEN gemini-2.5-flash falha por quota, THE System SHALL tentar gemini-2.5-flash-lite
3. WHEN todos os modelos falham, THE System SHALL reportar erro detalhado
4. THE System SHALL registrar qual modelo foi usado com sucesso

### Requirement 3: Monitoramento de Quota

**User Story:** Como administrador, eu quero monitorar o uso da quota do Gemini, para planejar a geração de questões adequadamente.

#### Acceptance Criteria

1. THE System SHALL rastrear quantas requisições foram feitas por modelo
2. WHEN a quota está próxima do limite, THE System SHALL alertar o usuário
3. WHEN a quota é esgotada, THE System SHALL calcular quando ela será resetada
4. THE System SHALL exibir estatísticas de uso em tempo real

### Requirement 4: Recuperação Automática

**User Story:** Como usuário, eu quero que o sistema se recupere automaticamente de falhas temporárias, para continuar a geração sem intervenção manual.

#### Acceptance Criteria

1. WHEN uma requisição falha por rate limit, THE System SHALL aguardar e tentar novamente
2. WHEN a quota diária é esgotada, THE System SHALL aguardar até o reset
3. WHEN há erro de rede temporário, THE System SHALL fazer retry com backoff exponencial
4. THE System SHALL limitar tentativas para evitar loops infinitos

### Requirement 5: Configuração de Produção

**User Story:** Como administrador, eu quero configurar facilmente as API keys no ambiente de produção, para que o sistema funcione no Render.

#### Acceptance Criteria

1. THE System SHALL ler API keys de variáveis de ambiente
2. WHEN no Render, THE System SHALL usar a GEMINI_API_KEY configurada
3. THE System SHALL validar configuração na inicialização
4. WHEN configuração está incorreta, THE System SHALL falhar rapidamente com erro claro