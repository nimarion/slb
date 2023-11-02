import pandas as pd

year = 2023

athletes = pd.read_csv('validate/' + str(year) + '/athletes.csv')
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
            

wrong_birthyear = data.merge(athletes, left_on=['firstname', 'lastname', 'club'], right_on=['firstname', 'lastname', 'club'])
wrong_birthyear = wrong_birthyear[wrong_birthyear['birthyear_x'] != wrong_birthyear['birthyear_y']]
wrong_birthyear.drop(columns=['birthyear_x'], inplace=True)
wrong_birthyear.rename(columns={'birthyear_y': 'birthyear'}, inplace=True)

for index, row in wrong_birthyear.iterrows():
    data.loc[(data['firstname'] == row['firstname']) & (data['lastname'] == row['lastname']) & (data['club'] == row['club']), 'birthyear'] = row['birthyear']

data.to_csv('data/' + str(year) + '.csv', index=False)
