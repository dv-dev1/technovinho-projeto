from datetime import date, time
import unittest

from frontend.lib import scheduling


class SchedulingTests(unittest.TestCase):
    def test_is_past_date_only_flags_dates_before_today(self):
        today = date(2026, 5, 23)

        self.assertTrue(scheduling.is_past_date(date(2026, 5, 22), today=today))
        self.assertFalse(scheduling.is_past_date(date(2026, 5, 23), today=today))
        self.assertFalse(scheduling.is_past_date(date(2026, 5, 24), today=today))

    def test_availability_for_date_returns_only_matching_weekday(self):
        selected = date(2026, 6, 1)  # Monday, Python weekday 0.
        rows = [
            {"day_of_week": 0, "start_time": "09:00:00", "end_time": "11:00:00"},
            {"day_of_week": 1, "start_time": "14:00:00", "end_time": "18:00:00"},
        ]

        self.assertEqual([rows[0]], scheduling.availability_for_date(rows, selected))

    def test_build_slot_options_generates_half_hour_slots_inside_ranges(self):
        rows = [
            {"day_of_week": 0, "start_time": "09:00:00", "end_time": "10:30:00"},
            {"day_of_week": 0, "start_time": "14:00:00", "end_time": "15:00:00"},
        ]

        slots = scheduling.build_slot_options(rows)

        self.assertEqual(
            [
                {"label": "09:00", "time": time(9, 0)},
                {"label": "09:30", "time": time(9, 30)},
                {"label": "10:00", "time": time(10, 0)},
                {"label": "14:00", "time": time(14, 0)},
                {"label": "14:30", "time": time(14, 30)},
            ],
            slots,
        )

    def test_combine_date_time_returns_iso_payload_value(self):
        self.assertEqual(
            "2026-06-01T14:30:00",
            scheduling.combine_date_time(date(2026, 6, 1), time(14, 30)),
        )

    def test_slot_options_fit_selected_service_duration(self):
        rows = [{"day_of_week": 0, "start_time": "09:00:00", "end_time": "10:00:00"}]

        slots = scheduling.build_slot_options(rows, duration_minutes=45)

        self.assertEqual([{"label": "09:00", "time": time(9, 0)}], slots)


if __name__ == "__main__":
    unittest.main()
