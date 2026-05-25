from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[2]
APP_FILE = ROOT / "frontend" / "app.py"


def test_login_page_renders_email_and_password_fields():
    app = AppTest.from_file(str(APP_FILE)).run()

    labels = [field.label for field in app.text_input]

    assert "Email" in labels
    assert "Senha" in labels


def test_seed_credentials_authenticate_user(monkeypatch):
    def fake_login(email, password):
        assert email == "cliente@test.com"
        assert password == "senha12345"
        return {"access_token": "fake-token"}

    def fake_me(token):
        assert token == "fake-token"
        return {"id": 1, "name": "Cliente Seed", "email": "cliente@test.com", "role": "client"}

    from frontend.lib import api
    import lib.api as runtime_api

    monkeypatch.setattr(api, "login", fake_login)
    monkeypatch.setattr(api, "me", fake_me)
    monkeypatch.setattr(runtime_api, "login", fake_login)
    monkeypatch.setattr(runtime_api, "me", fake_me)

    app = AppTest.from_file(str(APP_FILE)).run()
    app.text_input[0].input("cliente@test.com")
    app.text_input[1].input("senha12345")
    app.button[0].click().run()

    assert app.session_state["token"] == "fake-token"
    assert app.session_state["user"]["name"] == "Cliente Seed"
    assert "Cliente: use" in app.success[0].value
