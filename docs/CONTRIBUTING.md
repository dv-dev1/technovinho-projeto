# Contribuindo — technovinho-projeto

## Regra principal

**Cada card do Trello (ou alteração entregável) → pelo menos um commit** na branch `feature/<slug>`.

Mensagem deve citar o card:

```
feat(escopo): resumo

Card Trello: [Nome] título do card
```

Documentação completa do time: repositório de gestão `Technovinho` → `docs/guardrails.md`.

## Fluxo

1. `git checkout develop && git pull`
2. `git checkout -b feature/nome-do-card`
3. Implementar + commit + push
4. PR para `develop`

Não commitar `.env` nem secrets.
