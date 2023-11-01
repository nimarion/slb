import pandas as pd

year = 2023

athletes = pd.read_csv('validate/' + str(year) + '/athletes.csv')
data = pd.read_csv('data/' + str(year) + '.csv')

# Create a new column in both DataFrames with the first two letters of the 'firstname'
data['firstname_2letters'] = data['firstname'].str[:2] + data['firstname'].str[-2:]
athletes['firstname_2letters'] = athletes['firstname'].str[:2] + athletes['firstname'].str[-2:]

# Merge DataFrames on 'firstname_2letters', 'lastname', and 'club'
merged_data = data.merge(athletes, on=['firstname_2letters', 'lastname', 'club', 'birthyear'])


# Filter out rows where 'lastname' from both DataFrames is not equal
filtered_data = merged_data[merged_data['firstname_x'] != merged_data['firstname_y']]

# Drop the 'firstname_2letters' column if no longer needed
filtered_data = filtered_data.drop('firstname_2letters', axis=1)
filtered_data.drop(columns=['athleteId', 'sex', 'country', 'result', 'location', 'teamResult', 'place', 'birthyear'], inplace=True)
filtered_data.rename(columns={'firstname_x': 'Vorname in Bestenliste', 'firstname_y': 'Vorname in Startrecht'}, inplace=True)

cols = list(filtered_data.columns.values)
cols.pop(cols.index('lastname'))
cols.pop(cols.index('Vorname in Bestenliste'))
cols.pop(cols.index('Vorname in Startrecht'))
filtered_data = filtered_data[cols+['lastname', 'Vorname in Bestenliste', 'Vorname in Startrecht']]

filtered_data.to_excel('tmp/wrong_firstname_' + str(year) + '.xlsx', index=False)

print(filtered_data)