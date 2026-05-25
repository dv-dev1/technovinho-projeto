from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_FILE = ROOT / "frontend" / "pages" / "5_Admin_Dashboard.py"


def test_admin_dashboard_blocks_client_role_from_session_state(monkeypatch):
    import frontend.lib.ui as ui
    import lib.ui as runtime_ui

    monkeypatch.setattr(ui, "sidebar_nav", lambda: None)
    monkeypatch.setattr(runtime_ui, "sidebar_nav", lambda: None)

    app = AppTest.from_file(str(DASHBOARD_FILE))
    app.session_state["token"] = "fake-token"
    app.session_state["user_role"] = "client"
    app.session_state["user_id"] = 1
    app.session_state["user_name"] = "Cliente Seed"
    app.session_state["user"] = None

    app.run()

    assert "Acesso restrito para este perfil." in app.warning[0].value


def test_sidebar_nav_links_to_admin_dashboard(monkeypatch):
    from frontend.lib import ui

    links = []

    class Sidebar:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    class FakeStreamlit:
        sidebar = Sidebar()

        @staticmethod
        def page_link(path, label, icon=None):
            links.append((path, label, icon))

    monkeypatch.setattr(ui, "st", FakeStreamlit)

    ui.sidebar_nav()

    assert ("pages/5_Admin_Dashboard.py", "Dashboard admin", None) in links
