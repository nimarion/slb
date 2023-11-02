import pandas as pd

year = 2023

athletes = pd.read_csv('validate/' + str(year) + '/athletes.csv')
data = pd.read_csv('data/' + str(year) + '.csv')

shortest = data['lastname'].str.len().min()

data['lastname_2letters'] = data['lastname'].str[:shortest]
athletes['lastname_2letters'] = athletes['lastname'].str[:shortest]

merged_data = data.merge(athletes, on=['lastname_2letters', 'firstname', 'club', 'birthyear'])


wrong_lastname = merged_data[merged_data['lastname_x'] != merged_data['lastname_y']]

# Anzahl möglicher anderer Nachnamen
counted_lastnames = athletes.groupby(['firstname', 'club', 'birthyear', 'lastname_2letters'])['lastname'].count().reset_index()
counted_lastnames.rename(columns={'lastname': 'Possible_Other_LastNames_Count'}, inplace=True)
wrong_lastname = wrong_lastname.merge(counted_lastnames, on=['firstname', 'club', 'birthyear', 'lastname_2letters'], how='left')
wrong_lastname = wrong_lastname[wrong_lastname['Possible_Other_LastNames_Count'] == 1]
wrong_lastname = wrong_lastname.drop('lastname_2letters', axis=1)
data = data.drop('lastname_2letters', axis=1)

for index, row in wrong_lastname.iterrows():
    data.loc[(data['lastname'] == row['lastname_x']) & (data['firstname'] == row['firstname']) & (data['club'] == row['club']), 'lastname'] = row['lastname_y']

data.to_csv('data/' + str(year) + '.csv', index=False)