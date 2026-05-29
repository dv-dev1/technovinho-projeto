# Evidencia - BUG-002 Confirmacao de agendamento

Card Trello: https://trello.com/c/EmCYvLzW/40-jos%C3%A9-bug-002-corrigir-teste-ui-de-confirma%C3%A7%C3%A3o-de-agendamento

## Correcao

- A disponibilidade do teste de confirmacao agora acompanha a data selecionada
  automaticamente pela pagina.
- O teste procura o botao por seu texto e valida a mensagem visivel sem depender
  de indices em colecoes possivelmente vazias.

## Evidencia

O log da validacao exigida no card esta em `pytest-frontend-ui.txt`.
