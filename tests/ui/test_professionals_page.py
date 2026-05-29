from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[2]
PROFESSIONALS_FILE = ROOT / "frontend" / "pages" / "1_Profissionais.py"
REGISTER_FILE = ROOT / "frontend" / "pages" / "0_Registro.py"


def test_register_page_only_creates_client_accounts():
    app = AppTest.from_file(str(REGISTER_FILE)).run()

    text_input_labels = [field.label for field in app.text_input]
    select_labels = [field.label for field in app.selectbox]

    assert "Nome" in text_input_labels
    assert "Perfil" not in select_labels
    assert not select_labels


def test_professionals_page_uses_barber_onboarding_form(monkeypatch):
    import frontend.lib.api as api
    import frontend.lib.ui as ui
    import lib.api as runtime_api
    import lib.ui as runtime_ui

    monkeypatch.setattr(api, "list_professionals", lambda token: [])
    monkeypatch.setattr(runtime_api, "list_professionals", lambda token: [])
    monkeypatch.setattr(ui, "sidebar_nav", lambda: None)
    monkeypatch.setattr(runtime_ui, "sidebar_nav", lambda: None)
    monkeypatch.setattr(ui, "page_header", lambda *args, **kwargs: None)
    monkeypatch.setattr(runtime_ui, "page_header", lambda *args, **kwargs: None)

    app = AppTest.from_file(str(PROFESSIONALS_FILE))
    app.session_state["token"] = "admin-token"
    app.session_state["user_role"] = "admin"
    app.session_state["user_id"] = 1
    app.session_state["user_name"] = "Admin"
    app.session_state["user"] = {"id": 1, "role": "admin", "name": "Admin"}
    app.run()

    labels = [field.label for field in app.text_input]

    assert "User ID do barbeiro" not in labels
    assert "Nome" in labels
    assert "Email" in labels
    assert "Senha inicial" in labels
