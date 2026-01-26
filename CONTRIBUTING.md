# Guia de Contribuição

Obrigado por considerar contribuir com o Sistema de Simulados IBGP!

## Como Contribuir

### Reportando Bugs
Use o template de Bug Report nas Issues.

### Sugerindo Funcionalidades
Use o template de Feature Request nas Issues.

### Adicionando Questões

#### Requisitos de Qualidade
Todas as questões devem:
1. Ter referência clara ao edital (página/artigo)
2. Seguir o estilo IBGP (formal, objetivo)
3. Ter 4 alternativas plausíveis
4. Incluir explicação detalhada
5. Passar na validação QA (score >= 80)

#### Processo
1. Fork o repositório
2. Crie uma branch: `git checkout -b questoes/nova-disciplina`
3. Adicione questões via API ou diretamente no banco
4. Execute validação: `python scripts/validate_questions.py`
5. Commit: `git commit -m "Add: 10 questões de Redes"`
6. Push: `git push origin questoes/nova-disciplina`
7. Abra Pull Request usando o template

#### Formato de Questão
```json
{
  "disciplina": "Redes",
  "topico": "Protocolos",
  "subtopico": "TCP/IP",
  "enunciado": "Sobre o protocolo TCP, é correto afirmar que:",
  "alternativa_a": "...",
  "alternativa_b": "...",
  "alternativa_c": "...",
  "alternativa_d": "...",
  "gabarito": "A",
  "explicacao_detalhada": "...",
  "referencia": "Edital página X",
  "dificuldade": "médio",
  "estimativa_tempo": 3,
  "keywords": ["redes", "tcp", "protocolo"]
}
```

### Revisando Questões

#### Checklist de Revisão
- [ ] Enunciado claro e objetivo
- [ ] Alternativas plausíveis (sem "pegadinhas" óbvias)
- [ ] Gabarito correto e verificável
- [ ] Explicação completa e didática
- [ ] Referência válida
- [ ] Sem erros de português
- [ ] Sem duplicidade

### Desenvolvimento

#### Setup Local
```bash
git clone <repo>
cd simulados-ibgp
cp .env.example .env
docker-compose up --build
```

#### Rodando Testes
```bash
# API
cd api
pytest tests/ -v

# Web
cd web
npm test
```

#### Style Guide
- Python: Black + Flake8
- JavaScript: ESLint
- Commits: Conventional Commits

#### Estrutura de Commits
```
feat: adiciona nova funcionalidade
fix: corrige bug
docs: atualiza documentação
test: adiciona testes
refactor: refatora código
style: ajustes de formatação
chore: tarefas de manutenção
```

## Código de Conduta
- Seja respeitoso
- Aceite críticas construtivas
- Foque no que é melhor para a comunidade
- Mostre empatia

## Dúvidas?
Abra uma Issue com a tag `question`.
