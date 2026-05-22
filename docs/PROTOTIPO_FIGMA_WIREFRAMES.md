# Prototipo Figma - Wireframes principais

Card Trello: [[Caue] Prototipo Figma (wireframes principais)](https://trello.com/c/b4vDXbdD/18-cau%C3%AA-prot%C3%B3tipo-figma-wireframes-principais)

Este pacote documenta os wireframes principais do TECHNOVINHO para reproducao no Figma. O arquivo visual editavel/importavel esta em [prototipo-figma-wireframes.svg](prototipo-figma-wireframes.svg).

Link Figma view-only: https://www.figma.com/design/O79fatjH5z0BStcQDUdwIv/Sem-t%C3%ADtulo?node-id=0-1&t=pxWPDhk6RPPRs3Ym-1

## Objetivo

Validar a navegacao principal antes/durante a implementacao em Streamlit, cobrindo autenticacao, jornada do cliente, agendamento e administracao.

## Componentes basicos

### Cores

| Token | Uso | Valor |
|---|---|---|
| `primary` | botoes principais, etapa ativa, links | `#7C2D12` |
| `primary_dark` | hover/realce forte | `#431407` |
| `accent` | badges, metricas e destaques | `#F59E0B` |
| `surface` | fundo da aplicacao | `#F8FAFC` |
| `card` | paineis, formularios e cards | `#FFFFFF` |
| `border` | divisorias e inputs | `#CBD5E1` |
| `text` | texto principal | `#111827` |
| `muted` | texto auxiliar | `#64748B` |
| `danger` | exclusao/erro | `#DC2626` |
| `success` | confirmacao/status positivo | `#16A34A` |

### Tipografia

- Fonte sugerida no Figma: Inter ou Sans Serif padrao.
- H1: 28 px, semibold.
- H2: 22 px, semibold.
- Texto de corpo: 16 px.
- Texto auxiliar: 13 px.
- Botoes: 15 px, semibold.

### Componentes

- Topbar com marca TECHNOVINHO, area/perfil atual e acao de sair.
- Sidebar administrativa com links: Dashboard, Servicos, Profissionais, Disponibilidade.
- Card de servico com nome, duracao, preco e botao de agendar.
- Stepper de agendamento com quatro etapas: Servico, Profissional, Horario, Confirmar.
- Tabela administrativa com busca, filtros, status e acoes.
- Modal/drawer simples para criar ou editar registros.
- Badge de status para agendamentos: confirmado, pendente, cancelado.

## Frames obrigatorios

| Frame | Tela | RF/RNF relacionado | Conteudo principal |
|---|---|---|---|
| 01 | Login | RF01, RNF01 | Email, senha, entrar, link para registro |
| 02 | Registro | RF01, RNF01 | Nome, email, senha, perfil cliente, criar conta |
| 03 | Home cliente / listagem servicos | Jornada cliente | Lista de servicos e chamada para agendar |
| 04 | Agendamento (steps) | Agendamento | Stepper com servico, profissional, horario e resumo |
| 05 | Confirmacao agendamento | Agendamento | Estado de sucesso com dados do atendimento |
| 06 | Meus agendamentos | Agendamento | Historico/lista com status e acao de cancelar |
| 07 | Dashboard admin | RF07 | 3 metricas: agendamentos hoje, receita prevista, ocupacao |
| 08 | CRUD servicos admin | RF07 | Tabela de servicos, criar, editar, excluir |
| 09 | CRUD profissionais admin | RF07 | Tabela de profissionais, especialidade/status e servicos |
| 10 | Grade disponibilidade | RF07 | Grade por profissional, dia e horarios livres/ocupados |

## Fluxo de navegacao

1. Usuario acessa Login.
2. Novo usuario segue para Registro e retorna autenticado para Home cliente.
3. Cliente escolhe um servico na Home e avanca para Agendamento.
4. Cliente passa pelo stepper: servico, profissional, horario e confirmacao.
5. Sistema exibe Confirmacao agendamento.
6. Cliente acompanha registros em Meus agendamentos.
7. Usuario admin acessa Dashboard admin.
8. Admin gerencia Servicos, Profissionais e Disponibilidade pela sidebar.

## Criterios de aceite do card

- Existe um artefato visual com os 10 frames obrigatorios: [prototipo-figma-wireframes.svg](prototipo-figma-wireframes.svg).
- Cada frame tem titulo identificavel e mapeamento para RF/RNF ou jornada correspondente.
- Os componentes basicos de cores e tipografia estao documentados.
- O README aponta para o link Figma view-only e para este pacote de prototipo.

## Observacao sobre Figma

O link Figma view-only foi registrado no README para atender ao entregavel do card. Este repositorio nao contem credenciais ou automacao de publicacao no Figma.
