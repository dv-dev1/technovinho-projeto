# Modelo de dados

O schema relacional e versionado por Alembic em `backend/alembic/versions/`.
As tabelas do contrato APS estao cobertas pelas migrations:

| Tabela | Relacoes principais |
| --- | --- |
| `users` | Email unico; perfis `admin`, `barber`, `client` |
| `services` | Catalogo de servicos ativos/inativos |
| `professionals` | `user_id` unico para usuario barbeiro |
| `availability` | Faixas semanais por profissional |
| `appointments` | Cliente, profissional e servico agendados |

## Integridade

- `users.email`, `appointments.client_id` e `appointments.scheduled_at` possuem indice.
- `availability.day_of_week` aceita somente `0` (segunda) a `6` (domingo).
- `availability.end_time` deve ser posterior a `availability.start_time`.
- O status de agendamento aceita `pending`, `confirmed`, `cancelled` e `done`.

## Decisoes de exclusao

As FKs de `appointments` para `users`, `professionals` e `services`, assim como
`professionals.user_id`, usam `RESTRICT`. Um registro envolvido em atendimento
nao pode ser removido e perder o historico da operacao.

`availability.professional_id` usa `CASCADE`: faixas de trabalho deixam de
existir quando o profissional e removido, pois nao sao registros historicos.

## Aplicacao

Em um banco vazio:

```bash
cd backend
alembic upgrade head
```

Esse comando cria o schema inicial e aplica as constraints complementares de
disponibilidade.
