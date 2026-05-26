import unittest
from unittest.mock import patch

import requests

from frontend.lib import api


class FakeResponse:
    def __init__(self, status_code=200, payload=None, text=""):
        self.status_code = status_code
        self._payload = payload
        self.text = text
        self.content = b"" if payload is None else b"{}"

    def json(self):
        if isinstance(self._payload, Exception):
            raise self._payload
        return self._payload


class ApiAuthTests(unittest.TestCase):
    @patch("frontend.lib.api.requests.request")
    def test_register_posts_to_auth_register(self, request):
        request.return_value = FakeResponse(
            201,
            {"id": 1, "name": "Cliente", "email": "cliente@test.com", "role": "client"},
        )

        result = api.register(
            {
                "name": "Cliente",
                "email": "cliente@test.com",
                "password": "senha12345",
                "role": "client",
            }
        )

        self.assertEqual("cliente@test.com", result["email"])
        request.assert_called_once()
        _, kwargs = request.call_args
        self.assertEqual("POST", request.call_args.args[0])
        self.assertTrue(request.call_args.args[1].endswith("/api/auth/register"))
        self.assertEqual(10, kwargs["timeout"])

    @patch("frontend.lib.api.requests.request")
    def test_authenticated_requests_send_bearer_token(self, request):
        request.return_value = FakeResponse(200, [])

        api.list_services("token-123")

        _, kwargs = request.call_args
        self.assertEqual({"Authorization": "Bearer token-123"}, kwargs["headers"])

    @patch("frontend.lib.api.requests.request")
    def test_login_401_uses_card_message(self, request):
        request.return_value = FakeResponse(401, {"detail": "qualquer"}, "qualquer")

        with self.assertRaises(api.ApiError) as err:
            api.login("cliente@test.com", "senha-errada")

        self.assertEqual(401, err.exception.status_code)
        self.assertEqual("Email ou senha invalidos.", err.exception.detail)

    @patch("frontend.lib.api.requests.request")
    def test_register_409_uses_card_message(self, request):
        request.return_value = FakeResponse(409, {"detail": "Email ja cadastrado"}, "conflict")

        with self.assertRaises(api.ApiError) as err:
            api.register(
                {
                    "name": "Cliente",
                    "email": "cliente@test.com",
                    "password": "senha12345",
                    "role": "client",
                }
            )

        self.assertEqual(409, err.exception.status_code)
        self.assertEqual("Email ja cadastrado.", err.exception.detail)

    @patch("frontend.lib.api.requests.request")
    def test_422_uses_friendly_validation_message(self, request):
        request.return_value = FakeResponse(422, {"detail": [{"msg": "bad"}]}, "bad")

        with self.assertRaises(api.ApiError) as err:
            api.login("email-invalido", "senha12345")

        self.assertEqual(422, err.exception.status_code)
        self.assertEqual("Dados invalidos. Confira os campos informados.", err.exception.detail)

    @patch("frontend.lib.api.requests.request")
    def test_connection_error_hides_stack_trace(self, request):
        request.side_effect = requests.exceptions.ConnectionError("offline")

        with self.assertRaises(api.ApiError) as err:
            api.login("cliente@test.com", "senha12345")

        self.assertEqual(0, err.exception.status_code)
        self.assertIn("API offline", err.exception.detail)
        self.assertNotIn("Traceback", err.exception.detail)


if __name__ == "__main__":
    unittest.main()
