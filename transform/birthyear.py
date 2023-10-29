import pandas as pd
import os

years = [int(file.split('.')[0])
         for file in os.listdir('data') if file.split('.')[0].isnumeric()]

for year in years:
    data = pd.read_csv('data/' + str(year) + '.csv')
    birthyear = data[data['birthyear'] == 0]
    if(len(birthyear) > 0):
        for index, row in birthyear.iterrows():
            first_name = row['firstname']
            last_name = row['lastname']
            club = row['club']

            other_entries = data[(data['firstname'] == first_name) & (
                data['lastname'] == last_name) & (data['club'] == club) & (data['birthyear'] != 0)]
            
            different_birth_years = other_entries['birthyear'].unique()
            if(len(different_birth_years) > 1):
                print(str(year) + ":" + str(len(different_birth_years)) +
                      " verschiedene Geburtsjahre für " + first_name + " " + last_name)
                print(other_entries[['athleteId', 'firstname', 'lastname', 'birthyear']])
            if len(other_entries) >= 1 and len(different_birth_years) == 1:
                birth_year_to_copy = other_entries.iloc[0]['birthyear']
                data.at[index, 'birthyear'] = birth_year_to_copy

        data.to_csv('data/' + str(year) + '.csv', index=False)
