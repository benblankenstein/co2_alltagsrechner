import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titel der App
st.title("CO₂-Alltagsrechner")

# Textanzeige
st.write("Kompensiere **ALLE** deine Emissionen. Dieser kleine Rechner berechnet die CO₂-eq-Emissionen, die im Alltag "
         "entstehen. Dabei werden die Emissionsquellen in Kategorien unterteilt: Ernährung, Verkehr, Konsum und "
         "Haushalt. Grundlage sind Daten aus der Probas-Datenbank. Diese Werte wurden durch verschiedene Annahmen in "
         "Werte umgerechnet, die im Alltag vorkommen. Der Rechner erhebt keinen Anspruch auf Vollständigkeit, sondern "
         "soll ein Gefühl dafür vermitteln, welche Handlungen im Alltag welche Emissionen verursachen.")

# Funktion zur Berechnung der CO2-Emissionen mit benutzerdefinierter Formel
def berechne_emissionen(input_wert, formel):
    try:
        wert = float(input_wert)
        return formel(wert)
    except ValueError:
        return 0

# Formeln für jede Aktivität (Lambda-Funktionen)
multiplikatoren = {
    "Strom und Heizwärme": lambda x: x * 4.7 * 0.405 + x * 12.2 * 0.236,
    "Warmwasser (Duschen)": lambda x: x * 3.5 + x * 0.000242,
    "Kochen": lambda x: x * 0.139 * 0.601,
    "Bus": lambda x: x * 0.0555,
    "PKW (Verbrenner)": lambda x: x * 0.16,
    "PKW (Elektro)": lambda x: x * 0.0479,
    "Zug": lambda x: x * 0.071,
    "Fahrrad": lambda x: x * 0.00407,
    "Bestellte Klamotten": lambda x: x * 0.25 * 36.6,
    "Gemüse": lambda x: x * 0.137,
    "Reis": lambda x: x * 4.85,
    "Äpfel": lambda x: x * 0.879 / 5,
    "Bananen": lambda x: x * 0.0392 / 8,
    "Rindfleisch": lambda x: x * 26,
    "Hähnchen": lambda x: x * 13.1,
    "Fisch": lambda x: x * 2.46,
    "Brot": lambda x: x * 35 / 1000 * 0.639,
    "Eier": lambda x: x * 60 / 1000 * 1.22,
    "Käse": lambda x: x * 30 / 1000 * 8.18,
    "Trinkwasser": lambda x: x * 0.000242,
    "Zeitungen/Bücher": lambda x: x * 350 / 1000 * (1.34 + 1.27) / 2
}

# Zuordnung zu Kategorien
kategorien = {
    "Essen": ["Gemüse", "Reis", "Äpfel", "Bananen", "Rindfleisch", "Hähnchen", "Fisch", "Brot", "Eier", "Käse"],
    "Transport": ["Bus", "PKW (Verbrenner)", "PKW (Elektro)", "Zug", "Fahrrad"],
    "Konsum": ["Bestellte Klamotten", "Zeitungen/Bücher"],
    "Haushalt": ["Strom und Heizwärme", "Warmwasser (Duschen)", "Kochen", "Trinkwasser"]
}

fragen = {
    "Strom und Heizwärme": "Wie lange ist dein betrachteter Zeitraum (in Tagen)?",
    "Warmwasser (Duschen)": "Wie oft hast du in diesem Zeitraum geduscht?",
    "Kochen": "Wie oft hast du in diesem Zeitraum warm gekocht?",
    "Bus": "Wie viele Kilometer bist du mit dem Bus gefahren?",
    "PKW (Verbrenner)": "Wie viele Kilometer bist du mit einem Verbrenner-PKW gefahren?",
    "PKW (Elektro)": "Wie viele Kilometer bist du mit einem Elektro-PKW gefahren?",
    "Zug": "Wie viele Kilometer bist du mit dem Zug gefahren?",
    "Fahrrad": "Wie viele Kilometer bist du Fahrrad gefahren?",
    "Bestellte Klamotten": "Wie viele Kleidungsstücke hast du bestellt?",
    "Gemüse": "Wie viele Kilogramm Gemüse hast du gegessen?",
    "Reis": "Wie viele Kilogramm Reis hast du gegessen?",
    "Äpfel": "Wie viele Äpfel hast du gegessen?",
    "Bananen": "Wie viele Bananen hast du gegessen?",
    "Rindfleisch": "Wie viele Kilogramm Rindfleisch hast du gegessen?",
    "Hähnchen": "Wie viele Kilogramm Hähnchen hast du gegessen?",
    "Fisch": "Wie viele Kilogramm Fisch hast du gegessen?",
    "Brot": "Wie viele Scheiben Brot hast du gegessen?",
    "Eier": "Wie viele Eier hast du gegessen?",
    "Käse": "Wie viele Scheiben Käse hast du gegessen?",
    "Trinkwasser": "Wie viele Liter Wasser hast du getrunken?",
    "Zeitungen/Bücher": "Wie viele Zeitungen/Bücher hast du gekauft?"
}

# Initialisierung der Emissionen mit 0
inputs = {}
gesamt_emissionen = {kategorie: {aktivität: 0 for aktivität in kategorien[kategorie]} for kategorie in kategorien}

# Eingabe sammeln und Berechnung durchführen
for key in multiplikatoren:
    frage = fragen[key]
    inputs[key] = st.text_input(frage, value="0")

    # Emissionen berechnen
    formel = multiplikatoren[key]
    input_value = inputs[key]
    emissionen = berechne_emissionen(input_value, formel)

    # Kategorie identifizieren und Emissionen hinzufügen
    for kategorie, aktivitäten in kategorien.items():
        if key in aktivitäten:
            gesamt_emissionen[kategorie][key] = emissionen

# Berechnung der Gesamt-Emissionen
gesamt_emissionen_kategorie = {kategorie: sum(gesamt_emissionen[kategorie].values()) for kategorie in gesamt_emissionen}
gesamt_emissionen_gesamt = sum(gesamt_emissionen_kategorie.values())

# Gesamt-Emissionen anzeigen
st.subheader(f"Gesamt-Emissionen: {gesamt_emissionen_gesamt:.2f} kg CO₂-eq")

# DataFrame erstellen
df = pd.DataFrame(gesamt_emissionen).fillna(0).T

# Diagramm erstellen
fig, ax = plt.subplots(figsize=(10, 6))
df.plot(kind="bar", stacked=True, ax=ax)

# Plot-Anpassungen
ax.set_ylabel("Emissionen (kg CO₂-eq)")
ax.set_xlabel("")
ax.set_title("CO₂-eq-Emissionen nach Kategorie")

# Legende: Kombinierte Legende mit Kategorien und Aktivitäten
handles, labels = ax.get_legend_handles_labels()

# Kombinierte Legende
ncol = 4  # Anzahl der Spalten in der Legende
ax.legend(handles=handles, labels=labels, title="Aktivitäten", bbox_to_anchor=(0.5, -0.25), loc="upper center",
          ncol=ncol)

# Balkendiagramm anzeigen
st.pyplot(fig)

# Button für Vereinfachungen / Annahmen
if st.button('Vereinfachungen / Annahmen anzeigen'):
    vereinfachungen_data = {
        "Energiebereitstellung": [
            ("Haushaltsstrom Durchschnitt Deutschland", "Jährlicher Stromverbrauch eines 1-Personen-Haushalts in Deutschland nach Gebäudetyp im Jahr 2023 (in Kilowattstunden), Statista, 2023"),
            ("Raumwärme Durchschnitt Deutschland", "3 oder Mehrpersonenhaushalt; Pro-Kopf-Energieverbrauch für Wohnen und Heizen 2019, Destatis, 2019"),
            ("Warmwasser Durchschnitt Deutschland", "3,5 kWh; Wasser von 10° auf 40° erwärmt bei 13l pro Minute"),
            ("Kochen mit Elektroherd", "4,19kJ für 1° Temperaturerhöhung bei einem 1kg Wasser; fürs Kochen von Kartoffeln ca. 500kJ (0,139kWh)")
        ],
        "Transportprozesse": [
            ("Linienbus", ""),
            ("Diesel-PKW-Kleinwagen", "Diesel und Benziner gemittelt, Kleinwagen"),
            ("E-Mobile-Kleinwagen", "Kleinwagen"),
            ("Benzin-PKW-Kleinwagen", "Diesel und Benziner gemittelt, Kleinwagen"),
            ("Zug im Nahverkehr - Diesellok", "Diesellok"),
            ("Fahrrad", "")
        ],
        "Lebensmittel": [
            ("Gemüse", ""),
            ("Reis", ""),
            ("Bananen", "Gewicht Apfel 200g"),
            ("Äpfel", "Gewicht Bananen 110g"),
            ("Rindfleisch", ""),
            ("Hähnchen", ""),
            ("Importierter Fisch", ""),
            ("Brot", "Gewicht Scheibe Brot 35g"),
            ("Eier", "Gewicht 1 Ei 60g"),
            ("Käse", "Gewicht Scheibe Käse 30g"),
            ("Milch", ""),
            ("Trinkwasser aus der Leitung", "Betrachtung nur Trinkwasser")

        ],
        "Biobasierten Produkten": [
            ("Herstellung Papier", "Mittelung Bücher und Zeitung, Gewicht 350g pro Buch"),
            ("Baumwoll-T-Shirt", "Gewicht Tshirt 250g, Vernachlässigung Transport"),
            ("Zeitungspapier", "Mittelung Bücher und Zeitung, Gewicht 350g pro Buch")
        ]
    }

    # Tabelle anzeigen in einem scrollbaren Bereich
    for category, data in vereinfachungen_data.items():
        with st.expander(category):
            vereinfachungen_df = pd.DataFrame(data, columns=["Energiebereitstellung", "Vereinfachung / Annahme"])
            st.dataframe(vereinfachungen_df, use_container_width=True)

# Button für den direkten Link zu Probas
if st.button('Link zu Probas'):
    js_code = "window.open('https://www.probas.umweltbundesamt.de/einblick/#/', '_blank')"
    st.components.v1.html(f"<script>{js_code}</script>", height=0)
