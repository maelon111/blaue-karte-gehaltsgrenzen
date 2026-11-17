"""python -m gehaltsgrenzen 48000 --engpass | python -m gehaltsgrenzen --tabelle"""
import argparse
import json
import sys

from . import BBG, STAND, grenzen, pruefen


def eur(x: float) -> str:
    return f"{x:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="gehaltsgrenzen",
                                description="Gehaltsgrenzen Blaue Karte EU und Fachkräfte ab 45 Jahren / "
                                            "German salary thresholds for the EU Blue Card")
    p.add_argument("gehalt", nargs="?", type=float, help="Bruttojahresgehalt in Euro / gross annual salary")
    p.add_argument("--jahr", type=int, default=max(BBG))
    p.add_argument("--engpass", action="store_true", help="Engpassberuf / shortage occupation")
    p.add_argument("--berufsanfaenger", action="store_true", help="Abschluss vor höchstens 3 Jahren / recent graduate")
    p.add_argument("--it-ohne-abschluss", action="store_true", help="IT-Fachkraft ohne Hochschulabschluss")
    p.add_argument("--fachkraft", action="store_true", help="Aufenthaltserlaubnis §§ 18a/18b statt Blaue Karte")
    p.add_argument("--alter", type=int, help="Alter bei Antragstellung / age")
    p.add_argument("--tabelle", action="store_true", help="alle Grenzen anzeigen / show all thresholds")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    if a.tabelle or a.gehalt is None:
        rows = [grenzen(j) for j in sorted(BBG)]
        if a.json:
            print(json.dumps(rows, indent=2))
            return 0
        print(f"Gehaltsgrenzen (brutto pro Jahr), Stand {STAND}")
        print(f"{'Jahr':<6}{'Blaue Karte':>16}{'Engpass/Anfänger':>20}{'Fachkraft ab 45':>18}")
        for r in rows:
            print(f"{r['jahr']:<6}{eur(r['blaue_karte_regel']):>16}{eur(r['blaue_karte_engpass']):>20}"
                  f"{eur(r['fachkraft_ab_45']):>18}")
        return 0
    try:
        e = pruefen(a.gehalt, a.jahr, engpassberuf=a.engpass, berufsanfaenger=a.berufsanfaenger,
                    it_ohne_abschluss=a.it_ohne_abschluss, alter=a.alter, weg="fachkraft" if a.fachkraft else "blaue_karte")
    except ValueError as exc:
        print(f"gehaltsgrenzen: {exc}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(e.to_dict(), ensure_ascii=False, indent=2))
    else:
        weg = "Aufenthaltserlaubnis §§ 18a/18b" if e.weg == "fachkraft" else "Blaue Karte EU"
        print(f"{weg} {e.jahr}: Schwelle {eur(e.schwelle)} brutto/Jahr ({eur(e.schwelle / 12)} pro Monat)")
        print(f"Gehalt {eur(e.bruttojahresgehalt)}: " + ("erfüllt ✔" if e.erfuellt else f"nicht erfüllt ✘ (es fehlen {eur(e.fehlbetrag)})"))
        print("Zustimmung der Bundesagentur für Arbeit: " + ("ja" if e.zustimmung_ba else "nein"))
        for h in e.hinweise:
            print(f"- {h}")
    return 0 if e.erfuellt else 1


if __name__ == "__main__":
    sys.exit(main())
