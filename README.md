# Leichtathletik Bestenlisten Auswertung

Eine Auswertung der Saarländischen Leichtathletik Bestenliste mit Juptyer Notebooks.

## Auswertunngen

- [top10.ipynb](top10.ipynb) - Auswertung der Top 10 Platzierungen
  - Bestenlistenpunkte pro Verein
  - Bestenlistenpunkte pro Jahrgang und Geschlecht
  - Bestenlistenpunkte pro Athlet
  - Bestenlistenpunkte pro Ort
  - Athleten pro Jahrgang
  - Durchschnittliches Alter in der Aktiven Klassen
  - Älteste Athleten in der Bestenliste
- [general.ipynb](general.ipynb) - Auswertung der gesamten Bestenliste (nur ab 2023 möglich, Rest enthält nur bis Daten bis Platz 10)
  - Jahresbestleistungen pro Ort
  - Jahresbestleistungen pro Tag
  - Jahresbestleistungen pro Verein  
  - Athleten pro Jahrgang
  - Athleten pro Verein und Anzahl der Jahresbestleistungen 
  - Älteste Athleten
- [compare.ipynb](compare.ipynb) -Jahresübergreifende Auswertung der Bestenliste (Top 10)
  - Athleten pro Jahr
  - Durchschnittsalter pro Jahr
  - Anzahl der Disziplinen pro Jahr
  - Anzahl der Vereine pro Jahr
  - Anzahl Wettkampforte pro Jahr
  - Athleten mit den meisten Bestenlistenpunkten
  - Athleten mit den meisten Einträgen in der Bestenliste
  - Athleten mit den meisten Vereinen
  - Athleten mit den meisten Disziplinen

Datenformat:
```csv
"club","discipline","firstname","lastname","birthyear","result","ageGroup","date","location","place","teamResult","athleteId"
```

athleteId ist erst ab 2023 vorhanden. Für Mannschafts oder Staffel Ergebnisse ist für jeden Teilnehmer eine Zeile vorhanden.
Die Zeile wird bei der Punkteauswerung für alle Verein nur einmal gezählt.

```python
data.drop_duplicates(subset=['ageGroup', 'club', 'discipline', 'result', 'teamResult', 'place', 'location', 'date'])
```

Genutzte Projekte:
- [Jupyter](https://jupyter.org/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)

Datenquellen:
- [2023](https://bestenliste.slb-saarland.com)
- [2020-2022](https://slb-saarland.com/)

