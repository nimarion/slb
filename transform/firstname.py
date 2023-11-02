import pandas as pd

year = 2023

athletes = pd.read_csv('validate/' + str(year) + '/athletes.csv')
data = pd.read_csv('data/' + str(year) + '.csv')


data['firstname_2letters'] = data['firstname'].str[:1]
athletes['firstname_2letters'] = athletes['firstname'].str[:1]

merged_data = data.merge(athletes, on=['firstname_2letters', 'lastname', 'club', 'birthyear'])

wrong_firstname = merged_data[merged_data['firstname_x'] != merged_data['firstname_y']]

# Anzahl möglicher anderer Vornamen
counted_firstnames = athletes.groupby(['lastname', 'club', 'birthyear', 'firstname_2letters'])['firstname'].count().reset_index()
counted_firstnames.rename(columns={'firstname': 'Possible_Other_FirstNames_Count'}, inplace=True)
wrong_firstname = wrong_firstname.merge(counted_firstnames, on=['lastname', 'club', 'birthyear', 'firstname_2letters'], how='left')
wrong_firstname = wrong_firstname[wrong_firstname['Possible_Other_FirstNames_Count'] == 1]
wrong_firstname = wrong_firstname.drop('firstname_2letters', axis=1)
data = data.drop('firstname_2letters', axis=1)

for index, row in wrong_firstname.iterrows():
    data.loc[(data['firstname'] == row['firstname_x']) & (data['lastname'] == row['lastname']) & (data['club'] == row['club']), 'firstname'] = row['firstname_y']

data.to_csv('data/' + str(year) + '.csv', index=False)