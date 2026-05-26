from datetime import date
import unittest

from frontend.lib import dashboard


class DashboardTests(unittest.TestCase):
    def test_today_appointments_keeps_only_selected_date(self):
        rows = [
            {"id": 1, "scheduled_at": "2026-05-23T09:00:00", "status": "pending"},
            {"id": 2, "scheduled_at": "2026-05-23T14:30:00+00:00", "status": "confirmed"},
            {"id": 3, "scheduled_at": "2026-05-24T10:00:00", "status": "pending"},
        ]

        result = dashboard.today_appointments(rows, today=date(2026, 5, 23))

        self.assertEqual([1, 2], [row["id"] for row in result])

    def test_estimated_revenue_ignores_cancelled_appointments(self):
        appointments = [
            {"service_id": 1, "status": "pending"},
            {"service_id": 2, "status": "confirmed"},
            {"service_id": 1, "status": "cancelled"},
            {"service_id": 999, "status": "pending"},
        ]
        services = [
            {"id": 1, "price": 35.0},
            {"id": 2, "price": 25.0},
        ]

        self.assertEqual(60.0, dashboard.estimated_revenue(appointments, services))

    def test_active_professionals_count_counts_only_active_records(self):
        professionals = [
            {"id": 1, "active": True},
            {"id": 2, "active": False},
            {"id": 3, "active": True},
        ]

        self.assertEqual(2, dashboard.active_professionals_count(professionals))

    def test_dashboard_rows_format_table_data(self):
        appointments = [
            {
                "id": 7,
                "client_name": "Cliente APS",
                "professional_name": "Barbeiro APS",
                "service_name": "Corte",
                "scheduled_at": "2026-05-23T09:00:00",
                "status": "pending",
            }
        ]

        self.assertEqual(
            [
                {
                    "ID": 7,
                    "Horario": "09:00",
                    "Cliente": "Cliente APS",
                    "Servico": "Corte",
                    "Profissional": "Barbeiro APS",
                    "Status": "Pendente",
                }
            ],
            dashboard.dashboard_rows(appointments),
        )


if __name__ == "__main__":
    unittest.main()
