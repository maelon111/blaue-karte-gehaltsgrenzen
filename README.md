# Gehaltsgrenzen 2026 — Blaue Karte EU und Fachkräfte ab 45 Jahren

**TL;DR** — Offene Daten und ein kleiner Rechner (Python, MIT-Lizenz): Erfüllt ein Bruttojahresgehalt die
Gehaltsgrenze für die **Blaue Karte EU** oder für die Aufenthaltserlaubnis als Fachkraft ab 45 Jahren? Für 2026 gelten
**50.700 €** (Regelfall), **45.934,20 €** (Engpassberufe, Berufsanfänger, IT-Fachkräfte ohne Studium) und
**55.770 €** (Fachkräfte nach §§ 18a/18b ab 45 Jahren). Stand: 14.11.2026.

*English summary below.*

## Gehaltsgrenzen (brutto pro Jahr)

| Jahr | BBG Rentenversicherung | Blaue Karte EU, Regelfall (50 %) | Engpassberufe, Berufsanfänger, IT ohne Abschluss (45,3 %) | Fachkraft §§ 18a/18b ab 45 Jahren (55 %) |
|---|---|---|---|---|
| 2024 | 90.600 € | 45.300,00 € | 41.041,80 € | 49.830,00 € |
| 2025 | 96.600 € | 48.300,00 € | 43.759,80 € | 53.130,00 € |
| **2026** | **101.400 €** | **50.700,00 €** (4.225 €/Monat) | **45.934,20 €** (3.827,85 €/Monat) | **55.770,00 €** (4.647,50 €/Monat) |

Maschinenlesbar: [`daten/gehaltsgrenzen.csv`](daten/gehaltsgrenzen.csv). Alle Werte sind feste Anteile der jährlichen
Beitragsbemessungsgrenze (BBG) der allgemeinen Rentenversicherung; die BBG ist seit 2025 bundesweit einheitlich
(2024: Wert West). Die Grenzen ändern sich jedes Jahr zum 1. Januar.

## Welche Grenze gilt?

- **Blaue Karte EU, Regelfall** (§ 18g Abs. 1 Satz 1 AufenthG): anerkannter oder vergleichbarer Hochschulabschluss,
  Gehalt mindestens 50 % der BBG. Keine Zustimmung der Bundesagentur für Arbeit (BA) nötig.
- **Abgesenkte Grenze, 45,3 %** (§ 18g Abs. 1 Satz 2 und Abs. 2 AufenthG): Engpassberufe (z. B. Ingenieure, Ärztinnen
  und Ärzte, Pflegefachkräfte, IT-Fachkräfte, Lehrkräfte), Berufsanfänger mit Abschluss in den letzten drei Jahren,
  IT-Fachkräfte ohne Studium mit mindestens drei Jahren Berufserfahrung in den letzten sieben Jahren. Mit Zustimmung
  der BA.
- **Fachkräfte nach §§ 18a/18b ab 45 Jahren** (§ 18 Abs. 2 Nr. 5 AufenthG): bei erstmaliger Erteilung mindestens 55 %
  der BBG, außer bei Nachweis einer angemessenen Altersversorgung. Unter 45 Jahren gibt es keine feste Grenze, das
  Gehalt muss aber dem vergleichbarer inländischer Beschäftigter entsprechen.

## Rechner

```bash
pip install git+https://github.com/maelon111/blaue-karte-gehaltsgrenzen
gehaltsgrenzen 48000 --engpass
```

```text
Blaue Karte EU 2026: Schwelle 45.934,20 € brutto/Jahr (3.827,85 € pro Monat)
Gehalt 48.000,00 €: erfüllt ✔
Zustimmung der Bundesagentur für Arbeit: ja
- Abgesenkte Grenze (45,3 % der BBG): Zustimmung der Bundesagentur für Arbeit erforderlich.
```

Weitere Optionen: `--berufsanfaenger`, `--it-ohne-abschluss`, `--fachkraft --alter 47`, `--jahr 2025`, `--tabelle`,
`--json`. In Python:

```python
from gehaltsgrenzen import pruefen
e = pruefen(48000, 2026, engpassberuf=True)
print(e.erfuellt, e.schwelle, e.zustimmung_ba)
```

Web-Oberfläche: `pip install gradio` und `python app.py`, oder online im
[Hugging Face Space](https://huggingface.co/spaces/RaphMael/blaue-karte-gehaltsgrenzen).

## FAQ

**Zählen Boni und variable Vergütung?** Maßgeblich ist das vertraglich zugesicherte Bruttojahresgehalt; variable
Bestandteile werden von den Behörden nur berücksichtigt, wenn sie garantiert sind. Im Zweifel bei der
Ausländerbehörde nachfragen.

**Gilt die Grenze des Antragsjahres?** Ja, entscheidend ist die Grenze zum Zeitpunkt der Entscheidung über den Antrag.
Ein Antrag im Dezember kann deshalb nach den Werten des folgenden Jahres beschieden werden.

**Und die Chancenkarte?** Die Chancenkarte (§ 20a AufenthG) ist eine Aufenthaltserlaubnis zur Arbeitsuche mit
Punktesystem und hat keine Gehaltsgrenze. Für die anschließende Beschäftigung gelten die Grenzen oben.

## Quellen

- Make it in Germany (Bundesregierung), Blaue Karte EU: https://www.make-it-in-germany.com/de/visum-aufenthalt/arten/blaue-karte-eu
- Aufenthaltsgesetz, § 18 und § 18g: https://www.gesetze-im-internet.de/aufenthg_2004/
- Sozialversicherungsrechengrößen-Verordnung 2026 (BBG 8.450 €/Monat, 101.400 €/Jahr)

Keine Rechtsberatung: Maßgeblich sind die Auskünfte der Ausländerbehörde, der deutschen Auslandsvertretung und der
Bundesagentur für Arbeit. Fehler oder neue Werte? Bitte ein Issue öffnen.

## Über

Veröffentlicht von Raphaël Sellami, Gründer von [HireSpeeder](https://hirespeeder.de/?utm_source=github&utm_medium=readme&utm_campaign=blaue-karte-gehaltsgrenzen):
HireSpeeder vermittelt qualifizierte internationale Fachkräfte mit Deutschkenntnissen an kleine und mittlere
Unternehmen in Deutschland, in Engpassberufen (IT, Pflege, Elektro, SHK, Bau, Logistik, Gastronomie …).

---

## English

Open data and a small calculator for Germany's 2026 salary thresholds: **EU Blue Card €50,700** gross per year
(standard), **€45,934.20** (shortage occupations, recent graduates, IT specialists without a degree, with Federal
Employment Agency approval), and **€55,770** for skilled-worker permits (§§ 18a/18b) first issued at age 45 or older.
All values are fixed shares of the pension insurance contribution ceiling (€101,400 in 2026). CSV in `daten/`,
CLI `gehaltsgrenzen 48000 --engpass`, MIT licence. Made by the founder of
[HireSpeeder](https://hirespeeder.de/?utm_source=github&utm_medium=readme&utm_campaign=blaue-karte-gehaltsgrenzen).
