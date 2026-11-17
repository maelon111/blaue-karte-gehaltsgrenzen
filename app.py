"""Hugging Face Space / lokale Web-Oberfläche: python app.py (benötigt gradio)."""
import gradio as gr

from gehaltsgrenzen import BBG, STAND, grenzen, pruefen

LINK = ("Internationale Fachkräfte mit Deutschkenntnissen für Ihr Unternehmen: "
        "[hirespeeder.de](https://hirespeeder.de/?utm_source=huggingface&utm_medium=space&utm_campaign=gehaltsgrenzen)")


def eur(x):
    return f"{x:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def run(gehalt, jahr, weg, engpass, anfaenger, it, alter):
    if not gehalt:
        return "Bitte ein Bruttojahresgehalt eingeben."
    e = pruefen(float(gehalt), int(jahr), engpassberuf=engpass, berufsanfaenger=anfaenger, it_ohne_abschluss=it,
                alter=int(alter) if alter else None, weg="fachkraft" if weg.startswith("Fachkraft") else "blaue_karte")
    out = [f"## {'✅ erfüllt' if e.erfuellt else '❌ nicht erfüllt'}",
           f"Schwelle {e.jahr}: **{eur(e.schwelle)}** brutto/Jahr ({eur(e.schwelle / 12)} pro Monat)"]
    if not e.erfuellt:
        out.append(f"Es fehlen **{eur(e.fehlbetrag)}** pro Jahr.")
    out.append(f"Zustimmung der Bundesagentur für Arbeit: **{'ja' if e.zustimmung_ba else 'nein'}**")
    out += [f"- {h}" for h in e.hinweise]
    out.append(f"\n_Stand {STAND}, keine Rechtsberatung._\n\n---\n{LINK}")
    return "\n\n".join(out)


rows = "\n".join(f"| {g['jahr']} | {eur(g['blaue_karte_regel'])} | {eur(g['blaue_karte_engpass'])} | {eur(g['fachkraft_ab_45'])} |"
                 for g in (grenzen(j) for j in sorted(BBG)))
with gr.Blocks(title="Gehaltsgrenzen Blaue Karte EU 2026") as demo:
    gr.Markdown("# Gehaltsgrenzen 2026: Blaue Karte EU und Fachkräfte ab 45\n"
                "| Jahr | Blaue Karte | Engpass / Berufsanfänger / IT | Fachkraft ab 45 |\n|---|---|---|---|\n" + rows +
                "\n\nQuellcode und Daten: [github.com/maelon111/blaue-karte-gehaltsgrenzen]"
                "(https://github.com/maelon111/blaue-karte-gehaltsgrenzen)")
    with gr.Row():
        with gr.Column():
            gehalt = gr.Number(label="Bruttojahresgehalt (€)", value=48000)
            jahr = gr.Dropdown([str(j) for j in sorted(BBG)], value=str(max(BBG)), label="Jahr")
            weg = gr.Radio(["Blaue Karte EU (§ 18g)", "Fachkraft (§§ 18a/18b)"], value="Blaue Karte EU (§ 18g)", label="Aufenthaltstitel")
            engpass = gr.Checkbox(label="Engpassberuf")
            anfaenger = gr.Checkbox(label="Berufsanfänger (Abschluss vor höchstens 3 Jahren)")
            it = gr.Checkbox(label="IT-Fachkraft ohne Hochschulabschluss")
            alter = gr.Number(label="Alter (nur für §§ 18a/18b)", value=None)
            go = gr.Button("Prüfen", variant="primary")
        with gr.Column():
            out = gr.Markdown()
    go.click(run, [gehalt, jahr, weg, engpass, anfaenger, it, alter], out)

if __name__ == "__main__":
    demo.launch()
