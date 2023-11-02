import pandas as pd
import os
import hashlib

years = [int(file.split('.')[0])
         for file in os.listdir('data') if file.split('.')[0].isnumeric()]

for year in years:
    data = pd.read_csv('data/' + str(year) + '.csv')
    birthyear = data[data['birthyear'] == 0]
    if(len(birthyear) > 0):
        print(str(year) + ":" + str(len(birthyear)) +
              " Athleten ohne Geburtsjahr")

    # dd.mm.yyyy
    mask = data['date'].str.match(r'\d{2}\.\d{2}.\d{4}')
    dates = data[~mask]

    if(len(dates) > 0):
        print(str(year) + ":" + str(len(dates)) +
              " Ergebnisse in falschem Datumsformat")

    data['computed_athleteId'] = data.apply(lambda row: hashlib.sha256(
        (str(row['firstname']) + str(row['lastname']) +
         str(row['birthyear'])).encode('utf-8')
    ).hexdigest(), axis=1)

    data['is_hash_match'] = data['computed_athleteId'] == data['athleteId']

    mismatches = data[~data['is_hash_match']]
    if(len(mismatches) > 0):
        print(str(year) + ":" + str(len(mismatches)) +
              " Athleten mit falscher athleteId")
        print(mismatches[['athleteId', 'computed_athleteId',
              'firstname', 'lastname', 'birthyear']])

    duplicates = data[data.duplicated(['firstname', 'lastname', 'date', 'discipline'])]
    duplicates = duplicates[~duplicates['teamResult']]
    if(len(duplicates) > 0):
        print(str(year) + ":" + str(len(duplicates)) +
              " Duplikate in der Datenbank")
        print(duplicates[['athleteId', 'date', 'discipline', 'firstname', 'lastname', 'ageGroup']])

    incomplete_firstnames = data[data['firstname'].str.match(r'.*\.$')]
    if(len(incomplete_firstnames) > 0):
      print(str(year) + ":" + str(len(incomplete_firstnames)) +
                  " Athleten mit unvollständigem Vornamen")
      print(incomplete_firstnames[['athleteId', 'birthyear' , 'club', 'firstname', 'lastname']])
