import pandas as pd

year = 2023

athletes = pd.read_csv('validate/' + str(year) + '/athletes.csv')
data = pd.read_csv('data/' + str(year) + '.csv')


shortest = data[data['firstname'].str.len() > 2]['firstname'].str.len().min()

data['firstname_2letters'] = data['firstname'].str[:shortest]
athletes['firstname_2letters'] = athletes['firstname'].str[:shortest]

merged_data = data.merge(athletes, on=['firstname_2letters', 'lastname', 'club', 'birthyear'])

filtered_data = merged_data[merged_data['firstname_x'] != merged_data['firstname_y']]

# Anzahl möglicher anderer Vornamen
counted_firstnames = athletes.groupby(['lastname', 'club', 'birthyear', 'firstname_2letters'])['firstname'].count().reset_index()
counted_firstnames.rename(columns={'firstname': 'Possible_Other_FirstNames_Count'}, inplace=True)
filtered_data = filtered_data.merge(counted_firstnames, on=['lastname', 'club', 'birthyear', 'firstname_2letters'], how='left')
filtered_data = filtered_data[filtered_data['Possible_Other_FirstNames_Count'] == 1]


filtered_data = filtered_data.drop('firstname_2letters', axis=1)
#filtered_data.drop(columns=['athleteId', 'sex', 'country', 'result', 'location', 'teamResult', 'place', 'birthyear'], inplace=True)
filtered_data.rename(columns={'firstname_x': 'Vorname in Bestenliste', 'firstname_y': 'Vorname in Startrecht'}, inplace=True)

cols = list(filtered_data.columns.values)
cols.pop(cols.index('lastname'))
cols.pop(cols.index('Vorname in Bestenliste'))
cols.pop(cols.index('Vorname in Startrecht'))
filtered_data = filtered_data[cols+['lastname', 'Vorname in Bestenliste', 'Vorname in Startrecht']]

filtered_data.rename(columns={'lastname': 'Nachname', 'club': 'Verein', 'date': 'Datum', 'ageGroup': 'Altersklasse', 'discipline': 'Disziplin'} , inplace=True)
filtered_data.to_excel('tmp/wrong_firstname_' + str(year) + '.xlsx', index=False)


print(filtered_data)