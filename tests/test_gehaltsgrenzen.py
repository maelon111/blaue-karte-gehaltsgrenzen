import csv
import unittest

from gehaltsgrenzen import DATEN, grenzen, pruefen
from gehaltsgrenzen.__main__ import main


class TestGrenzen(unittest.TestCase):
    def test_2026(self):
        g = grenzen(2026)
        self.assertEqual((g["blaue_karte_regel"], g["blaue_karte_engpass"], g["fachkraft_ab_45"]),
                         (50700.0, 45934.2, 55770.0))

    def test_csv_matches_formula(self):
        with open(DATEN, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                g = grenzen(int(row["jahr"]))
                self.assertAlmostEqual(g["blaue_karte_regel"], float(row["blaue_karte_regel"]))
                self.assertAlmostEqual(g["blaue_karte_engpass"], float(row["blaue_karte_engpass_berufsanfaenger"]))
                self.assertAlmostEqual(g["fachkraft_ab_45"], float(row["fachkraft_ab_45"]))

    def test_unknown_year(self):
        with self.assertRaises(ValueError):
            grenzen(2019)


class TestPruefen(unittest.TestCase):
    def test_regel(self):
        e = pruefen(48000)
        self.assertFalse(e.erfuellt)
        self.assertEqual(e.fehlbetrag, 2700.0)
        self.assertFalse(e.zustimmung_ba)

    def test_engpass_needs_ba(self):
        e = pruefen(48000, engpassberuf=True)
        self.assertTrue(e.erfuellt)
        self.assertTrue(e.zustimmung_ba)

    def test_ab_45(self):
        self.assertFalse(pruefen(52000, weg="fachkraft", alter=47).erfuellt)
        self.assertTrue(pruefen(52000, weg="fachkraft", alter=30).erfuellt)

    def test_cli(self):
        self.assertEqual(main(["51000"]), 0)
        self.assertEqual(main(["40000", "--engpass"]), 1)
        self.assertEqual(main(["--tabelle"]), 0)
        self.assertEqual(main(["50000", "--jahr", "2019"]), 2)


if __name__ == "__main__":
    unittest.main()
