import unittest
from unittest.mock import patch

from frontend.lib import api
from tests.frontend.test_api_auth import FakeResponse


class ProfessionalsApiTests(unittest.TestCase):
    @patch("frontend.lib.api.requests.request")
    def test_create_professional_posts_barber_onboarding_payload(self, request):
        payload = {
            "name": "Barbeiro Novo",
            "email": "barbeiro@test.com",
            "password": "senha12345",
            "specialty": "Degrade",
            "active": True,
        }
        request.return_value = FakeResponse(201, {"id": 1, "user_id": 2, **payload})

        api.create_professional("admin-token", payload)

        self.assertEqual("POST", request.call_args.args[0])
        self.assertTrue(request.call_args.args[1].endswith("/api/professionals"))
        self.assertEqual({"Authorization": "Bearer admin-token"}, request.call_args.kwargs["headers"])
        self.assertEqual(payload, request.call_args.kwargs["json"])

    @patch("frontend.lib.api.requests.request")
    def test_update_professional_patches_specialty_and_active(self, request):
        payload = {"specialty": "Degrade", "active": False}
        request.return_value = FakeResponse(200, {"id": 1, "name": "Barbeiro", **payload})

        api.update_professional("admin-token", 1, payload)

        self.assertEqual("PATCH", request.call_args.args[0])
        self.assertTrue(request.call_args.args[1].endswith("/api/professionals/1"))
        self.assertEqual({"Authorization": "Bearer admin-token"}, request.call_args.kwargs["headers"])
        self.assertEqual(payload, request.call_args.kwargs["json"])


if __name__ == "__main__":
    unittest.main()
