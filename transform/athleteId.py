import pandas as pd
import hashlib

# Alle Athleten wird eine eindeutige ID zugewiesen die aus Vorname, Nachname und Geburtsjahr besteht um Daten über Jahre hinweg zu verknüpfen
# Startpassnummer ändert sich bei Vereinswechsel, daher nicht geeignet
year = 2023
data = pd.read_csv('data/' + str(year) + '.csv')
data['athleteId'] = data.apply(lambda row: hashlib.sha256(
        (str(row['firstname']) + str(row['lastname']) + str(row['birthyear'])).encode('utf-8')
    ).hexdigest(), axis=1)
data.to_csv('data/' + str(year) + '.csv', index=False)