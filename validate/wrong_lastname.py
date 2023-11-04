import pandas as pd

year = 2023

athletes = pd.read_csv('validate/' + str(year) + '/athletes.csv')
data = pd.read_csv('data/' + str(year) + '.csv')

shortest = data['lastname'].str.len().min()

data['lastname_2letters'] = data['lastname'].str[:shortest]
athletes['lastname_2letters'] = athletes['lastname'].str[:shortest]

merged_data = data.merge(athletes, on=['lastname_2letters', 'firstname', 'club', 'birthyear'])


filtered_data = merged_data[merged_data['lastname_x'] != merged_data['lastname_y']]

# Anzahl möglicher anderer Nachnamen
counted_firstnames = athletes.groupby(['firstname', 'club', 'birthyear', 'lastname_2letters'])['lastname'].count().reset_index()
counted_firstnames.rename(columns={'lastname': 'Possible_Other_LastNames_Count'}, inplace=True)
filtered_data = filtered_data.merge(counted_firstnames, on=['firstname', 'club', 'birthyear', 'lastname_2letters'], how='left')
filtered_data = filtered_data[filtered_data['Possible_Other_LastNames_Count'] == 1]
filtered_data = filtered_data[filtered_data.apply(lambda row: row['ageGroup'][0].replace('F', 'W') == row['sex'], axis=1)]


filtered_data = filtered_data.drop('lastname_2letters', axis=1)
filtered_data.drop(columns=['athleteId', 'sex', 'country', 'result', 'location', 'teamResult', 'place', 'birthyear'], inplace=True)

filtered_data.rename(columns={'lastname_x': 'Nachname in Bestenliste', 'lastname_y': 'Nachname in Startrecht'}, inplace=True)

cols = list(filtered_data.columns.values)
cols.pop(cols.index('firstname'))
cols.pop(cols.index('Nachname in Bestenliste'))
cols.pop(cols.index('Nachname in Startrecht'))
filtered_data = filtered_data[cols+['firstname', 'Nachname in Bestenliste', 'Nachname in Startrecht']]

#filtered_data = filtered_data.drop_duplicates(subset=['firstname', 'Nachname in Bestenliste', 'Nachname in Startrecht'], keep='first')


filtered_data.to_excel('tmp/wrong_lastname_' + str(year) + '.xlsx', index=False)

print(filtered_data)