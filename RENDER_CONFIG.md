# Configuração do Render - IMPORTANTE

## Variáveis de Ambiente para Adicionar

Acesse o dashboard do Render e adicione estas variáveis no serviço da API:

### API Backend (simulados-ibgp)

```
GEMINI_API_KEY=[SUA_CHAVE_AQUI]
```

**Como adicionar:**
1. Acesse: https://dashboard.render.com
2. Clique no serviço "simulados-ibgp" (API)
3. Vá em "Environment"
4. Clique em "Add Environment Variable"
5. Key: `GEMINI_API_KEY`
6. Value: `[SUA_CHAVE_AQUI]`
7. Clique em "Save Changes"
8. O serviço vai fazer redeploy automaticamente

## Verificar se funcionou

Após o redeploy, teste:
```
GET https://simulados-ibgp.onrender.com/api/health
```

Deve retornar status 200 com informações do sistema.
