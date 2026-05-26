import csv
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
JMETER_DIR = ROOT / "tests" / "jmeter"


class JMeterRNF03PlanTests(unittest.TestCase):
    def setUp(self):
        self.tree = ET.parse(JMETER_DIR / "technovinho.jmx")
        self.root = self.tree.getroot()

    def _thread_group(self, name: str):
        for element in self.root.iter("ThreadGroup"):
            if element.attrib.get("testname") == name:
                return element
        self.fail(f"ThreadGroup nao encontrado: {name}")

    def test_get_appointments_scenario_matches_rnf03_load(self):
        group = self._thread_group("Cenario 1 - GET appointments")

        self.assertEqual("50", group.findtext("stringProp[@name='ThreadGroup.num_threads']"))
        self.assertEqual("10", group.findtext("stringProp[@name='ThreadGroup.ramp_time']"))
        self.assertIn("/api/appointments", ET.tostring(self.root, encoding="unicode"))

    def test_post_appointments_scenario_matches_rnf03_load(self):
        group = self._thread_group("Cenario 2 - POST appointments")

        self.assertEqual("20", group.findtext("stringProp[@name='ThreadGroup.num_threads']"))
        self.assertEqual("5", group.findtext("stringProp[@name='ThreadGroup.ramp_time']"))
        self.assertIn("${scheduled_at}", ET.tostring(self.root, encoding="unicode"))

    def test_post_appointments_csv_has_enough_unique_rows(self):
        with (JMETER_DIR / "appointments.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))

        values = [row["scheduled_at"] for row in rows]
        self.assertGreaterEqual(len(values), 60)
        self.assertEqual(len(values), len(set(values)))


if __name__ == "__main__":
    unittest.main()
