import unittest
from unittest.mock import patch

from frontend.lib import api
from tests.frontend.test_api_auth import FakeResponse


class ServicesApiTests(unittest.TestCase):
    @patch("frontend.lib.api.requests.request")
    def test_list_services_is_public(self, request):
        request.return_value = FakeResponse(200, [])

        api.list_services()

        _, kwargs = request.call_args
        self.assertEqual({}, kwargs["headers"])

    @patch("frontend.lib.api.requests.request")
    def test_create_service_posts_payload_with_admin_token(self, request):
        payload = {"name": "Corte", "duration": 30, "price": 45.0, "active": True}
        request.return_value = FakeResponse(201, {"id": 1, **payload})

        result = api.create_service("admin-token", payload)

        self.assertEqual("Corte", result["name"])
        self.assertEqual("POST", request.call_args.args[0])
        self.assertTrue(request.call_args.args[1].endswith("/api/services"))
        self.assertEqual({"Authorization": "Bearer admin-token"}, request.call_args.kwargs["headers"])
        self.assertEqual(payload, request.call_args.kwargs["json"])

    @patch("frontend.lib.api.requests.request")
    def test_update_service_patches_active_flag(self, request):
        request.return_value = FakeResponse(200, {"id": 1, "active": False})

        api.update_service("admin-token", 1, {"active": False})

        self.assertEqual("PATCH", request.call_args.args[0])
        self.assertTrue(request.call_args.args[1].endswith("/api/services/1"))
        self.assertEqual({"active": False}, request.call_args.kwargs["json"])

    @patch("frontend.lib.api.requests.request")
    def test_update_service_sends_full_edit_payload(self, request):
        payload = {
            "name": "Corte Premium",
            "description": "Inclui lavagem",
            "duration": 50,
            "price": 60.0,
            "active": True,
        }
        request.return_value = FakeResponse(200, {"id": 1, **payload})

        api.update_service("admin-token", 1, payload)

        self.assertEqual({"Authorization": "Bearer admin-token"}, request.call_args.kwargs["headers"])
        self.assertEqual(payload, request.call_args.kwargs["json"])


if __name__ == "__main__":
    unittest.main()
