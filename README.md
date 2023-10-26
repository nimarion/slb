# Leichtathletik Bestenlisten Auswertung

Eine Auswertung der Saarländischen Leichtathletik Bestenliste mit Juptyer Notebooks.

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

