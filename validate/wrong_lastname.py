import pandas as pd

year = 2023

athletes = pd.read_csv('validate/' + str(year) + '/athletes.csv')
data = pd.read_csv('data/' + str(year) + '.csv')

# Create a new column in both DataFrames with the first two letters of the 'lastname'
data['lastname_2letters'] = data['lastname'].str[:2] + data['lastname'].str[-2:]
athletes['lastname_2letters'] = athletes['lastname'].str[:2] + athletes['lastname'].str[-2:]

# Merge DataFrames on 'lastname_2letters', 'lastname', and 'club'
merged_data = data.merge(athletes, on=['lastname_2letters', 'firstname', 'club', 'birthyear'])


# Filter out rows where 'lastname' from both DataFrames is not equal
filtered_data = merged_data[merged_data['lastname_x'] != merged_data['lastname_y']]

# Drop the 'lastname_2letters' column if no longer needed
filtered_data = filtered_data.drop('lastname_2letters', axis=1)
filtered_data.drop(columns=['athleteId', 'sex', 'country', 'result', 'location', 'teamResult', 'place'], inplace=True)
filtered_data.rename(columns={'lastname_x': 'Nachname in Bestenliste', 'lastname_y': 'Nachname in Startrecht'}, inplace=True)

cols = list(filtered_data.columns.values)
cols.pop(cols.index('firstname'))
cols.pop(cols.index('Nachname in Bestenliste'))
cols.pop(cols.index('Nachname in Startrecht'))
filtered_data = filtered_data[cols+['firstname', 'Nachname in Bestenliste', 'Nachname in Startrecht']]

filtered_data.to_excel('tmp/wrong_lastname_' + str(year) + '.xlsx', index=False)

print(filtered_data)