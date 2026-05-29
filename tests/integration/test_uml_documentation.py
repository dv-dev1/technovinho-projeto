from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "UML_DOCUMENTACAO_COMPLETA.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_uml_documentation_exists_and_has_acceptance_traceability():
    content = read_doc()

    assert "# Documentacao UML completa - TECHNOVINHO" in content
    assert "## Criterios de aceite" in content
    assert "## Rastreabilidade para arquivos do projeto" in content
    assert "Atendido" in content


def test_uml_documentation_has_required_diagram_types():
    content = read_doc()

    required_sections = [
        "## Diagrama de componentes",
        "## Diagrama de implantacao",
        "## Diagrama ER",
        "## Diagrama de classes de dominio",
        "## Casos de uso por perfil",
        "## Estados do agendamento",
    ]

    for section in required_sections:
        assert section in content

    assert content.count("```mermaid") >= 9
    assert "sequenceDiagram" in content
    assert "classDiagram" in content
    assert "erDiagram" in content
    assert "stateDiagram-v2" in content


def test_uml_documentation_covers_core_domain_and_flows():
    content = read_doc()

    for term in [
        "User",
        "Service",
        "Professional",
        "Availability",
        "Appointment",
        "AppointmentStatus",
        "UserRole",
        "POST /api/auth/login",
        "POST /api/appointments",
        "PATCH /api/appointments/{id}/cancel",
        "PATCH /api/services/{id}",
    ]:
        assert term in content


def test_uml_documentation_references_real_project_files():
    content = read_doc()

    for path in [
        "backend/app/main.py",
        "backend/app/routers/appointments.py",
        "backend/app/services/appointment_service.py",
        "backend/app/models/appointment.py",
        "frontend/app.py",
        "docker-compose.yml",
    ]:
        assert path in content
        assert (ROOT / path).exists()
