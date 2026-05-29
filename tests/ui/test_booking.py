from datetime import date, datetime
from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[2]
BOOKING_FILE = ROOT / "frontend" / "pages" / "4_Agendar.py"


def authenticated_booking_app():
    app = AppTest.from_file(str(BOOKING_FILE))
    app.session_state["token"] = "fake-token"
    app.session_state["user"] = {
        "id": 1,
        "name": "Cliente Seed",
        "email": "cliente@test.com",
        "role": "client",
    }
    return app


def disable_sidebar_nav(monkeypatch):
    try:
        import frontend.lib.ui as ui
        import lib.ui as runtime_ui
    except ModuleNotFoundError:
        return

    monkeypatch.setattr(ui, "sidebar_nav", lambda: None)
    monkeypatch.setattr(runtime_ui, "sidebar_nav", lambda: None)


def test_services_are_visible_after_login(monkeypatch):
    import frontend.lib.api as api
    import lib.api as runtime_api

    disable_sidebar_nav(monkeypatch)

    services = [
        {"id": 1, "name": "Corte masculino", "duration": 30, "price": 35.0, "active": True}
    ]
    professionals = [
        {"id": 1, "name": "Barbeiro Seed", "specialty": "Corte", "active": True}
    ]
    availability = [{"day_of_week": 0, "start_time": "09:00", "end_time": "10:00"}]

    monkeypatch.setattr(api, "list_services", lambda token: services)
    monkeypatch.setattr(api, "list_active_professionals", lambda token: professionals)
    monkeypatch.setattr(api, "list_availability", lambda token, professional_id: availability)
    monkeypatch.setattr(runtime_api, "list_services", lambda token: services)
    monkeypatch.setattr(runtime_api, "list_active_professionals", lambda token: professionals)
    monkeypatch.setattr(runtime_api, "list_availability", lambda token, professional_id: availability)

    app = authenticated_booking_app().run()

    assert "Corte masculino" in app.selectbox[0].options[0]


def test_booking_form_validates_empty_required_options(monkeypatch):
    import frontend.lib.api as api
    import lib.api as runtime_api

    disable_sidebar_nav(monkeypatch)

    monkeypatch.setattr(api, "list_services", lambda token: [])
    monkeypatch.setattr(api, "list_active_professionals", lambda token: [])
    monkeypatch.setattr(runtime_api, "list_services", lambda token: [])
    monkeypatch.setattr(runtime_api, "list_active_professionals", lambda token: [])

    app = authenticated_booking_app().run()

    assert "Nenhum servico ativo disponivel para agendamento." in app.info[0].value


def test_successful_booking_shows_confirmation_text(monkeypatch):
    import frontend.lib.api as api
    import frontend.lib.scheduling as scheduling
    import lib.api as runtime_api
    import lib.scheduling as runtime_scheduling

    disable_sidebar_nav(monkeypatch)

    today = date.today()
    services = [
        {"id": 1, "name": "Corte masculino", "duration": 30, "price": 35.0, "active": True}
    ]
    professionals = [
        {"id": 1, "name": "Barbeiro Seed", "specialty": "Corte", "active": True}
    ]
    availability = [{"day_of_week": today.weekday(), "start_time": "09:00", "end_time": "10:00"}]
    fake_now = datetime.combine(today, datetime.min.time()).replace(hour=8, minute=0)

    def fake_create_appointment(token, payload):
        assert payload["professional_id"] == 1
        assert payload["service_id"] == 1
        return {
            "id": 99,
            "status": "pending",
            "service_name": "Corte masculino",
            "professional_name": "Barbeiro Seed",
            "scheduled_at": payload["scheduled_at"],
            "notes": payload["notes"],
        }

    monkeypatch.setattr(api, "list_services", lambda token: services)
    monkeypatch.setattr(api, "list_active_professionals", lambda token: professionals)
    monkeypatch.setattr(api, "list_availability", lambda token, professional_id: availability)
    monkeypatch.setattr(api, "create_appointment", fake_create_appointment)
    monkeypatch.setattr(runtime_api, "list_services", lambda token: services)
    monkeypatch.setattr(runtime_api, "list_active_professionals", lambda token: professionals)
    monkeypatch.setattr(runtime_api, "list_availability", lambda token, professional_id: availability)
    monkeypatch.setattr(runtime_api, "create_appointment", fake_create_appointment)
    monkeypatch.setattr(scheduling, "datetime", type("FrozenDateTime", (), {"now": staticmethod(lambda: fake_now), "combine": datetime.combine}))
    monkeypatch.setattr(runtime_scheduling, "datetime", type("FrozenDateTime", (), {"now": staticmethod(lambda: fake_now), "combine": datetime.combine}))

    app = authenticated_booking_app().run()
    app.button[0].click().run()

    assert app.session_state["last_booking"]["id"] == 99
    assert "Agendamento solicitado." in app.success[0].value


def test_today_booking_hides_past_slots(monkeypatch):
    import frontend.lib.api as api
    import frontend.lib.scheduling as scheduling
    import lib.api as runtime_api
    import lib.scheduling as runtime_scheduling

    disable_sidebar_nav(monkeypatch)

    today = date.today()
    services = [
        {"id": 1, "name": "Corte masculino", "duration": 30, "price": 35.0, "active": True}
    ]
    professionals = [
        {"id": 1, "name": "Barbeiro Seed", "specialty": "Corte", "active": True}
    ]
    availability = [{"day_of_week": today.weekday(), "start_time": "09:00", "end_time": "11:00"}]
    fake_now = datetime.combine(today, datetime.min.time()).replace(hour=10, minute=15)

    monkeypatch.setattr(api, "list_services", lambda token: services)
    monkeypatch.setattr(api, "list_active_professionals", lambda token: professionals)
    monkeypatch.setattr(api, "list_availability", lambda token, professional_id: availability)
    monkeypatch.setattr(runtime_api, "list_services", lambda token: services)
    monkeypatch.setattr(runtime_api, "list_active_professionals", lambda token: professionals)
    monkeypatch.setattr(runtime_api, "list_availability", lambda token, professional_id: availability)
    monkeypatch.setattr(scheduling, "datetime", type("FrozenDateTime", (), {"now": staticmethod(lambda: fake_now), "combine": datetime.combine}))
    monkeypatch.setattr(runtime_scheduling, "datetime", type("FrozenDateTime", (), {"now": staticmethod(lambda: fake_now), "combine": datetime.combine}))

    app = authenticated_booking_app().run()

    assert app.selectbox[2].options == ["10:30"]
