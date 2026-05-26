import unittest
from unittest.mock import patch

from frontend.lib import api
from tests.frontend.test_api_auth import FakeResponse


class HistoryApiTests(unittest.TestCase):
    @patch("frontend.lib.api.requests.request")
    def test_history_requests_only_done_appointments(self, request):
        request.return_value = FakeResponse(200, [])

        api.list_appointments("token", status="done", mine=True)

        self.assertEqual({"status": "done", "mine": "true"}, request.call_args.kwargs["params"])

    @patch("frontend.lib.api.requests.request")
    def test_admin_can_complete_appointment(self, request):
        request.return_value = FakeResponse(200, {"id": 7, "status": "done"})

        result = api.complete_appointment("admin-token", 7)

        self.assertEqual("done", result["status"])
        self.assertEqual("PATCH", request.call_args.args[0])
        self.assertTrue(request.call_args.args[1].endswith("/api/appointments/7/complete"))


if __name__ == "__main__":
    unittest.main()
