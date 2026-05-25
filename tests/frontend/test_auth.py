import unittest

from frontend.lib import auth, ui


class FakeStop(Exception):
    pass


class FakeStreamlit:
    def __init__(self):
        self.session_state = {}
        self.warnings = []

    def warning(self, message):
        self.warnings.append(message)

    def stop(self):
        raise FakeStop()


class AuthHelperTests(unittest.TestCase):
    def test_validate_register_form_accepts_valid_client_registration(self):
        errors = auth.validate_register_form(
            name="Cliente Teste",
            email="cliente@test.com",
            password="senha12345",
            confirm_password="senha12345",
        )

        self.assertEqual([], errors)

    def test_validate_register_form_reports_card_required_rules(self):
        errors = auth.validate_register_form(
            name="C",
            email="email-invalido",
            password="curta",
            confirm_password="diferente",
        )

        self.assertIn("Informe um nome com pelo menos 2 caracteres.", errors)
        self.assertIn("Informe um email valido.", errors)
        self.assertIn("A senha deve ter pelo menos 8 caracteres.", errors)
        self.assertIn("As senhas devem ser iguais.", errors)

    def test_set_authenticated_session_stores_required_card_fields(self):
        st = FakeStreamlit()

        auth.set_authenticated_session(
            "token-123",
            {"id": 7, "name": "Caue", "email": "caue@test.com", "role": "client"},
            st_module=st,
        )

        self.assertEqual("token-123", st.session_state["token"])
        self.assertEqual("client", st.session_state["user_role"])
        self.assertEqual(7, st.session_state["user_id"])
        self.assertEqual("Caue", st.session_state["user_name"])
        self.assertEqual("client", st.session_state["user"]["role"])
        self.assertNotIn("password", st.session_state)

    def test_logout_clears_auth_session_fields(self):
        st = FakeStreamlit()
        st.session_state.update(
            {
                "token": "token-123",
                "user_role": "client",
                "user_id": 7,
                "user_name": "Caue",
                "user": {"id": 7},
                "appointment_confirmation": {"id": 1},
            }
        )

        auth.logout(st_module=st)

        for key in (
            "token",
            "user_role",
            "user_id",
            "user_name",
            "user",
            "appointment_confirmation",
        ):
            self.assertNotIn(key, st.session_state)

    def test_require_auth_blocks_missing_token(self):
        st = FakeStreamlit()

        with self.assertRaises(FakeStop):
            ui.require_auth(st_module=st)

        self.assertEqual(["Faca login na pagina inicial para continuar."], st.warnings)

    def test_require_auth_blocks_wrong_role(self):
        st = FakeStreamlit()
        st.session_state.update({"token": "token-123", "user_role": "client"})

        with self.assertRaises(FakeStop):
            ui.require_auth(["admin"], st_module=st)

        self.assertEqual(["Acesso restrito para este perfil."], st.warnings)


if __name__ == "__main__":
    unittest.main()
