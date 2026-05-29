from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_FILE = ROOT / "frontend" / "pages" / "5_Admin_Dashboard.py"


def test_admin_dashboard_blocks_client_role_from_session_state(monkeypatch):
    import frontend.lib.ui as ui
    import lib.ui as runtime_ui

    monkeypatch.setattr(ui, "sidebar_nav", lambda: None)
    monkeypatch.setattr(runtime_ui, "sidebar_nav", lambda: None)
    monkeypatch.setattr(ui, "page_header", lambda *args, **kwargs: None)
    monkeypatch.setattr(runtime_ui, "page_header", lambda *args, **kwargs: None)

    app = AppTest.from_file(str(DASHBOARD_FILE))
    app.session_state["token"] = "fake-token"
    app.session_state["user_role"] = "client"
    app.session_state["user_id"] = 1
    app.session_state["user_name"] = "Cliente Seed"
    app.session_state["user"] = None

    app.run()

    assert "Acesso restrito para este perfil." in app.warning[0].value


def test_nav_items_include_admin_dashboard_only_for_admin():
    from frontend.lib.ui import nav_items_for_role

    admin_labels = [item["label"] for item in nav_items_for_role("admin")]
    client_labels = [item["label"] for item in nav_items_for_role("client")]

    assert "Dashboard admin" in admin_labels
    assert "Dashboard admin" not in client_labels


def test_nav_items_give_barber_operational_links():
    from frontend.lib.ui import nav_items_for_role

    barber_labels = [item["label"] for item in nav_items_for_role("barber")]

    assert barber_labels == ["Inicio", "Minha agenda", "Historico"]
