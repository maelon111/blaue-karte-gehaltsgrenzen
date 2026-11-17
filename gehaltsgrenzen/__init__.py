"""Gehaltsgrenzen für ausländische Fachkräfte in Deutschland (Blaue Karte EU, §§ 18a/18b AufenthG ab 45 Jahren).

Alle Schwellen sind feste Anteile der jährlichen Beitragsbemessungsgrenze der allgemeinen Rentenversicherung (BBG):
- Blaue Karte EU, Regelfall (§ 18g Abs. 1 Satz 1 AufenthG): 50 % der BBG
- Blaue Karte EU, Engpassberufe, Berufsanfänger (Abschluss vor höchstens 3 Jahren) und IT-Fachkräfte ohne
  Hochschulabschluss (§ 18g Abs. 1 Satz 2 und Abs. 2 AufenthG): 45,3 % der BBG, mit Zustimmung der Bundesagentur für Arbeit
- Aufenthaltserlaubnis als Fachkraft nach §§ 18a/18b, erstmalige Erteilung ab 45 Jahren (§ 18 Abs. 2 Nr. 5 AufenthG):
  55 % der BBG, außer bei Nachweis einer angemessenen Altersversorgung
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, asdict
from pathlib import Path

__version__ = "1.0.0"
STAND = "2026-11-14"
DATEN = Path(__file__).resolve().parent.parent / "daten" / "gehaltsgrenzen.csv"

# BBG der allgemeinen Rentenversicherung (seit 2025 bundesweit einheitlich; 2024: Wert West)
BBG = {2024: 90600, 2025: 96600, 2026: 101400}
ANTEIL_REGEL, ANTEIL_ENGPASS, ANTEIL_AB_45 = 0.50, 0.453, 0.55


def grenzen(jahr: int) -> dict:
    if jahr not in BBG:
        raise ValueError(f"Keine Daten für {jahr} (verfügbar: {', '.join(map(str, sorted(BBG)))})")
    b = BBG[jahr]
    return {"jahr": jahr, "bbg": b, "blaue_karte_regel": round(b * ANTEIL_REGEL, 2),
            "blaue_karte_engpass": round(b * ANTEIL_ENGPASS, 2), "fachkraft_ab_45": round(b * ANTEIL_AB_45, 2)}


@dataclass
class Ergebnis:
    jahr: int
    bruttojahresgehalt: float
    weg: str
    schwelle: float
    erfuellt: bool
    fehlbetrag: float
    zustimmung_ba: bool
    hinweise: list

    def to_dict(self):
        return asdict(self)


def pruefen(bruttojahresgehalt: float, jahr: int = 2026, *, engpassberuf: bool = False, berufsanfaenger: bool = False,
            it_ohne_abschluss: bool = False, alter: int | None = None, weg: str = "blaue_karte") -> Ergebnis:
    """Prüft ein Bruttojahresgehalt gegen die passende Schwelle.

    weg = "blaue_karte" (§ 18g) oder "fachkraft" (§§ 18a/18b, nur die Altersgrenze ab 45 Jahren ist gehaltsgebunden).
    """
    g = grenzen(jahr)
    hinweise = []
    if weg == "fachkraft":
        if alter is not None and alter >= 45:
            schwelle = g["fachkraft_ab_45"]
            hinweise.append("Ab 45 Jahren: 55 % der BBG, außer bei Nachweis einer angemessenen Altersversorgung "
                            "(§ 18 Abs. 2 Nr. 5 AufenthG).")
        else:
            schwelle = 0.0
            hinweise.append("Unter 45 Jahren gibt es für §§ 18a/18b keine feste Gehaltsgrenze; das Gehalt muss aber "
                            "den Bedingungen vergleichbarer inländischer Beschäftigter entsprechen.")
        zustimmung = True
        hinweise.append("In der Regel ist die Zustimmung der Bundesagentur für Arbeit erforderlich.")
    elif weg == "blaue_karte":
        reduziert = engpassberuf or berufsanfaenger or it_ohne_abschluss
        schwelle = g["blaue_karte_engpass"] if reduziert else g["blaue_karte_regel"]
        zustimmung = reduziert
        if reduziert:
            hinweise.append("Abgesenkte Grenze (45,3 % der BBG): Zustimmung der Bundesagentur für Arbeit erforderlich.")
        if it_ohne_abschluss:
            hinweise.append("IT-Fachkräfte ohne Hochschulabschluss: mindestens drei Jahre vergleichbare Berufserfahrung "
                            "in den letzten sieben Jahren.")
        if berufsanfaenger:
            hinweise.append("Berufsanfänger: Hochschulabschluss innerhalb der letzten drei Jahre vor der Antragstellung.")
        if not reduziert and bruttojahresgehalt < g["blaue_karte_regel"] and bruttojahresgehalt >= g["blaue_karte_engpass"]:
            hinweise.append("Steht der Beruf auf der Liste der Engpassberufe für die Blaue Karte (z. B. Ingenieure, "
                            "Ärztinnen und Ärzte, Pflegefachkräfte, IT-Fachkräfte, Lehrkräfte), gilt die abgesenkte "
                            "Grenze.")
    else:
        raise ValueError("weg muss 'blaue_karte' oder 'fachkraft' sein")
    fehl = max(0.0, round(schwelle - bruttojahresgehalt, 2))
    return Ergebnis(jahr, bruttojahresgehalt, weg, schwelle, fehl == 0, fehl, zustimmung, hinweise)


def tabelle() -> list[dict]:
    with open(DATEN, encoding="utf-8") as f:
        return list(csv.DictReader(f))
