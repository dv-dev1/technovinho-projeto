# Documentacao UML completa - TECHNOVINHO

Responsavel: Pedro Lucas
Sprint: 4
Base revisada: `develop` em 2026-05-27

## Objetivo

Registrar a visao UML completa da solucao TECHNOVINHO a partir da estrutura
atual do codigo, cobrindo arquitetura, implantacao, dominio, banco de dados,
casos de uso, fluxos principais e estados de agendamento.

## Criterios de aceite

| Criterio | Status | Evidencia |
| --- | --- | --- |
| Documentar arquitetura geral da solucao | Atendido | Diagrama de componentes |
| Documentar deploy Docker Compose | Atendido | Diagrama de implantacao |
| Documentar entidades e relacionamentos | Atendido | Diagramas ER e classes de dominio |
| Documentar casos de uso por perfil | Atendido | Diagrama de casos de uso |
| Documentar fluxos principais | Atendido | Diagramas de sequencia |
| Documentar estados do agendamento | Atendido | Diagrama de estados |
| Rastrear a documentacao aos arquivos reais | Atendido | Secao de rastreabilidade |

## Escopo funcional coberto

- Autenticacao e autorizacao por JWT.
- Cadastro e login de usuarios.
- CRUD de servicos por administrador.
- Cadastro e manutencao de profissionais por administrador.
- Cadastro e consulta de disponibilidade por profissional.
- Agendamento por cliente.
- Cancelamento por cliente ou administrador.
- Conclusao de atendimento por administrador.
- Dashboard administrativo e historico de agendamentos.
- Validacoes de seguranca, disponibilidade, conflito e desempenho.

## Diagrama de componentes

```mermaid
flowchart LR
    UserClient["Cliente"]
    UserAdmin["Administrador"]
    UserBarber["Barbeiro"]

    subgraph Frontend["Frontend Streamlit :8501"]
        App["app.py"]
        Pages["pages/*.py"]
        ApiClient["lib/api.py"]
        AuthUi["lib/auth.py"]
        SchedulingUi["lib/scheduling.py"]
        DashboardUi["lib/dashboard.py"]
    end

    subgraph Backend["Backend FastAPI :8000"]
        Main["app/main.py"]
        Routers["routers"]
        Services["services"]
        Schemas["schemas"]
        Models["models"]
        Security["core/security.py"]
        Deps["core/deps.py"]
    end

    subgraph Database["PostgreSQL 15 :5432"]
        Pg["technovinho database"]
        Alembic["Alembic migrations"]
    end

    UserClient --> Pages
    UserAdmin --> Pages
    UserBarber --> Pages
    App --> Pages
    Pages --> ApiClient
    Pages --> AuthUi
    Pages --> SchedulingUi
    Pages --> DashboardUi
    ApiClient -->|HTTP JSON + Bearer JWT| Main
    Main --> Routers
    Routers --> Deps
    Deps --> Security
    Routers --> Services
    Routers --> Schemas
    Services --> Models
    Services --> Pg
    Alembic --> Pg
```

## Diagrama de implantacao

```mermaid
flowchart TB
    Browser["Navegador do usuario"]

    subgraph Compose["Docker Compose"]
        Frontend["frontend\nStreamlit\nporta 8501"]
        Api["api\nFastAPI/Uvicorn\nporta 8000"]
        Db["db\nPostgreSQL 15\nporta 5432"]
        Volume["pgdata"]
        Network["technovinho-net"]
    end

    Browser -->|HTTP :8501| Frontend
    Frontend -->|API_BASE_URL=http://api:8000| Api
    Api -->|DATABASE_URL| Db
    Db --> Volume
    Frontend --- Network
    Api --- Network
    Db --- Network
```

## Diagrama ER

```mermaid
erDiagram
    USERS {
        int id PK
        string name
        string email UK
        string password
        enum role
        datetime created_at
    }

    SERVICES {
        int id PK
        string name
        text description
        int duration
        numeric price
        boolean active
    }

    PROFESSIONALS {
        int id PK
        int user_id FK
        string specialty
        boolean active
    }

    AVAILABILITY {
        int id PK
        int professional_id FK
        int day_of_week
        time start_time
        time end_time
    }

    APPOINTMENTS {
        int id PK
        int client_id FK
        int professional_id FK
        int service_id FK
        datetime scheduled_at
        enum status
        text notes
        datetime created_at
    }

    USERS ||--o| PROFESSIONALS : "barber profile"
    USERS ||--o{ APPOINTMENTS : "client"
    PROFESSIONALS ||--o{ AVAILABILITY : "has weekly slots"
    PROFESSIONALS ||--o{ APPOINTMENTS : "performs"
    SERVICES ||--o{ APPOINTMENTS : "booked service"
```

## Diagrama de classes de dominio

```mermaid
classDiagram
    class UserRole {
        <<enumeration>>
        admin
        barber
        client
    }

    class AppointmentStatus {
        <<enumeration>>
        pending
        confirmed
        cancelled
        done
    }

    class User {
        +int id
        +str name
        +str email
        +str password
        +UserRole role
        +datetime created_at
    }

    class Service {
        +int id
        +str name
        +str description
        +int duration
        +Decimal price
        +bool active
    }

    class Professional {
        +int id
        +int user_id
        +str specialty
        +bool active
    }

    class Availability {
        +int id
        +int professional_id
        +int day_of_week
        +time start_time
        +time end_time
    }

    class Appointment {
        +int id
        +int client_id
        +int professional_id
        +int service_id
        +datetime scheduled_at
        +AppointmentStatus status
        +str notes
        +datetime created_at
    }

    UserRole <-- User
    AppointmentStatus <-- Appointment
    User "1" --> "0..1" Professional
    User "1" --> "0..*" Appointment : client
    Professional "1" --> "0..*" Availability
    Professional "1" --> "0..*" Appointment
    Service "1" --> "0..*" Appointment
```

## Diagrama de camadas do backend

```mermaid
flowchart TB
    Routes["FastAPI routers\n/auth, /services, /professionals,\n/availability, /appointments"]
    Deps["core/deps.py\nget_current_user, require_roles"]
    Schemas["Pydantic schemas\nentrada e saida HTTP"]
    Services["Application services\nregras de negocio"]
    Models["SQLAlchemy models\nentidades persistidas"]
    Session["db/session.py\nSession SQLAlchemy"]
    Security["core/security.py\nbcrypt + JWT"]
    Db["PostgreSQL"]

    Routes --> Deps
    Routes --> Schemas
    Routes --> Services
    Deps --> Security
    Services --> Models
    Services --> Session
    Session --> Db
```

## Casos de uso por perfil

```mermaid
flowchart LR
    Client["Cliente"]
    Admin["Administrador"]
    Barber["Barbeiro"]

    Register(("Cadastrar conta"))
    Login(("Realizar login"))
    ViewServices(("Consultar servicos"))
    Book(("Criar agendamento"))
    ViewMine(("Consultar meus agendamentos"))
    CancelMine(("Cancelar agendamento proprio"))

    ManageServices(("Gerenciar servicos"))
    ManageProfessionals(("Gerenciar profissionais"))
    ManageAvailability(("Gerenciar disponibilidade"))
    ViewDashboard(("Consultar dashboard"))
    Complete(("Concluir atendimento"))
    CancelAny(("Cancelar qualquer agendamento"))

    ViewProfessionalAgenda(("Consultar agenda associada"))

    Client --> Register
    Client --> Login
    Client --> ViewServices
    Client --> Book
    Client --> ViewMine
    Client --> CancelMine

    Admin --> Login
    Admin --> ManageServices
    Admin --> ManageProfessionals
    Admin --> ManageAvailability
    Admin --> ViewDashboard
    Admin --> Complete
    Admin --> CancelAny

    Barber --> Register
    Barber --> Login
    Barber --> ViewProfessionalAgenda
```

## Sequencia: cadastro e login

```mermaid
sequenceDiagram
    actor Usuario
    participant UI as Streamlit
    participant API as FastAPI auth router
    participant Auth as auth_service
    participant Sec as security
    participant DB as PostgreSQL

    Usuario->>UI: Preenche cadastro
    UI->>API: POST /api/auth/register
    API->>Auth: register_user(data)
    Auth->>DB: verifica email existente
    Auth->>Sec: hash_password(password)
    Auth->>DB: persiste User
    DB-->>Auth: User
    Auth-->>API: UserOut
    API-->>UI: 201 UserOut

    Usuario->>UI: Informa email e senha
    UI->>API: POST /api/auth/login
    API->>Auth: authenticate_user(data)
    Auth->>DB: busca User por email
    Auth->>Sec: verify_password()
    Auth->>Sec: create_access_token(user_id, role)
    Auth-->>API: token
    API-->>UI: TokenOut
    UI->>API: GET /api/auth/me
    API-->>UI: UserOut
```

## Sequencia: agendamento pelo cliente

```mermaid
sequenceDiagram
    actor Cliente
    participant UI as Streamlit Agendar
    participant API as appointments router
    participant Deps as auth dependency
    participant Appt as appointment_service
    participant Avail as availability_service
    participant DB as PostgreSQL

    Cliente->>UI: Seleciona servico, profissional, data e horario
    UI->>API: POST /api/appointments com Bearer JWT
    API->>Deps: get_current_user()
    Deps-->>API: User client
    API->>Appt: create_appointment(current_user, data)
    Appt->>DB: valida Service ativo
    Appt->>DB: valida Professional ativo
    Appt->>Avail: is_slot_available()
    Avail->>DB: consulta availability
    Avail-->>Appt: horario disponivel
    Appt->>DB: verifica conflito de agenda
    Appt->>DB: persiste Appointment pending
    Appt-->>API: AppointmentOut enriquecido
    API-->>UI: 201 AppointmentOut
    UI-->>Cliente: Exibe confirmacao
```

## Sequencia: cancelamento e conclusao

```mermaid
sequenceDiagram
    actor Usuario
    participant UI as Streamlit
    participant API as appointments router
    participant Deps as auth dependency
    participant Appt as appointment_service
    participant DB as PostgreSQL

    Usuario->>UI: Solicita cancelamento
    UI->>API: PATCH /api/appointments/{id}/cancel
    API->>Deps: get_current_user()
    API->>Appt: cancel_appointment(id, current_user)
    Appt->>DB: carrega Appointment
    Appt->>Appt: valida dono ou admin
    Appt->>Appt: valida prazo minimo CANCEL_MIN_HOURS
    Appt->>DB: status = cancelled
    API-->>UI: AppointmentOut atualizado

    Usuario->>UI: Admin conclui atendimento
    UI->>API: PATCH /api/appointments/{id}/complete
    API->>Deps: require_roles(admin)
    API->>Appt: complete_appointment(id)
    Appt->>DB: carrega Appointment
    Appt->>Appt: rejeita futuro, cancelled ou done
    Appt->>DB: status = done
    API-->>UI: AppointmentOut atualizado
```

## Sequencia: CRUD de servicos

```mermaid
sequenceDiagram
    actor Admin
    participant UI as Streamlit Servicos
    participant API as services router
    participant Deps as role guard
    participant Svc as service_service
    participant DB as PostgreSQL

    Admin->>UI: Preenche servico
    UI->>API: POST /api/services
    API->>Deps: require_roles(admin)
    API->>Svc: create_service(data)
    Svc->>DB: persiste Service
    API-->>UI: 201 ServiceOut

    Admin->>UI: Edita ou ativa/inativa servico
    UI->>API: PATCH /api/services/{id}
    API->>Deps: require_roles(admin)
    API->>Svc: update_service(id, data)
    Svc->>DB: atualiza Service
    API-->>UI: ServiceOut
```

## Sequencia: profissionais e disponibilidade

```mermaid
sequenceDiagram
    actor Admin
    participant UI as Streamlit Profissionais/Disponibilidade
    participant API as professionals router
    participant Deps as role guard
    participant Prof as professional_service
    participant Avail as availability_service
    participant DB as PostgreSQL

    Admin->>UI: Cadastra profissional para usuario barbeiro
    UI->>API: POST /api/professionals
    API->>Deps: require_roles(admin)
    API->>Prof: create_professional(data)
    Prof->>DB: valida User role barber
    Prof->>DB: persiste Professional
    API-->>UI: ProfessionalOut

    Admin->>UI: Cadastra faixa semanal
    UI->>API: POST /api/professionals/{id}/availability
    API->>Deps: require_roles(admin)
    API->>Avail: create_slot(professional_id, data)
    Avail->>DB: valida Professional existente
    Avail->>Avail: valida horario e sobreposicao
    Avail->>DB: persiste Availability
    API-->>UI: AvailabilityOut
```

## Estados do agendamento

```mermaid
stateDiagram-v2
    [*] --> pending : create_appointment
    pending --> cancelled : cancel_appointment
    pending --> done : complete_appointment apos horario
    confirmed --> cancelled : cancel_appointment
    confirmed --> done : complete_appointment apos horario
    cancelled --> [*]
    done --> [*]
```

## Navegacao e responsabilidades do frontend

```mermaid
flowchart TB
    Home["app.py\nlogin e sessao"]
    Register["0_Registro.py\ncadastro"]
    Professionals["1_Profissionais.py\nadmin profissionais"]
    Availability["2_Disponibilidade.py\nadmin faixas"]
    MyAppointments["3_Meus_Agendamentos.py\ncliente historico atual"]
    Booking["4_Agendar.py\ncliente agenda"]
    Dashboard["5_Admin_Dashboard.py\nadmin indicadores"]
    Services["6_Servicos.py\nadmin catalogo"]
    History["7_Historico.py\nhistorico concluido"]
    Api["lib/api.py\ncliente HTTP"]
    Auth["lib/auth.py\nsessao e validacao"]
    Ui["lib/ui.py\nguards e erros"]

    Home --> Register
    Home --> Professionals
    Home --> Availability
    Home --> MyAppointments
    Home --> Booking
    Home --> Dashboard
    Home --> Services
    Home --> History

    Register --> Api
    Booking --> Api
    MyAppointments --> Api
    Dashboard --> Api
    Services --> Api
    Professionals --> Api
    Availability --> Api
    History --> Api

    Home --> Auth
    Register --> Auth
    Professionals --> Ui
    Availability --> Ui
    MyAppointments --> Ui
    Booking --> Ui
    Dashboard --> Ui
    Services --> Ui
    History --> Ui
```

## Regras de negocio representadas

- Somente `client` cria agendamento.
- Somente `admin` cria/edita servicos.
- Somente `admin` cria/edita profissionais e disponibilidade.
- Um profissional deve estar vinculado a usuario com role `barber`.
- Um usuario barbeiro possui no maximo um registro em `professionals`.
- Um agendamento precisa de servico ativo, profissional ativo e horario futuro.
- O horario precisa caber na disponibilidade semanal do profissional.
- Agendamentos nao cancelados nao podem se sobrepor para o mesmo profissional.
- Cancelamento respeita `CANCEL_MIN_HOURS`.
- Atendimento futuro nao pode ser marcado como concluido.

## Rastreabilidade para arquivos do projeto

| Tema | Arquivos |
| --- | --- |
| API principal | `backend/app/main.py` |
| Autenticacao | `backend/app/routers/auth.py`, `backend/app/services/auth_service.py`, `backend/app/core/security.py` |
| Guards de seguranca | `backend/app/core/deps.py` |
| Servicos | `backend/app/routers/services.py`, `backend/app/services/service_service.py`, `backend/app/models/service.py` |
| Profissionais | `backend/app/routers/professionals.py`, `backend/app/services/professional_service.py`, `backend/app/models/professional.py` |
| Disponibilidade | `backend/app/routers/availability.py`, `backend/app/services/availability_service.py`, `backend/app/models/availability.py` |
| Agendamentos | `backend/app/routers/appointments.py`, `backend/app/services/appointment_service.py`, `backend/app/models/appointment.py` |
| Usuarios | `backend/app/models/user.py`, `backend/app/schemas/auth.py` |
| Banco e migrations | `backend/alembic/versions/`, `docs/MODELO_DADOS.md` |
| Frontend Streamlit | `frontend/app.py`, `frontend/pages/*.py`, `frontend/lib/*.py` |
| Deploy | `docker-compose.yml`, `backend/Dockerfile`, `frontend/Dockerfile` |
| Testes de apoio | `tests/integration/`, `tests/frontend/`, `tests/ui/` |

## Observacoes

- Os diagramas foram escritos em Mermaid para serem renderizados diretamente em
  plataformas compatveis com Markdown, como GitHub.
- Esta documentacao representa o estado atual do codigo no momento da task.
- Alteracoes futuras em rotas, modelos, regras de negocio ou telas devem
  atualizar este documento.
