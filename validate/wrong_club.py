import pandas as pd

year = 2023

athletes = pd.read_csv('validate/' + str(year) + '/athletes.csv')
data = pd.read_csv('data/' + str(year) + '.csv')

data = data.merge(athletes, left_on=['firstname', 'lastname', 'birthyear'], right_on=['firstname', 'lastname', 'birthyear'])
data = data[data['club_x'] != data['club_y']]
data = data[~data['club_x'].str.contains('StG')]
data.drop(columns=['athleteId', 'sex', 'country', 'result', 'ageGroup', 'date', 'location', 'teamResult'], inplace=True)
data.rename(columns={'club_x': 'Verein in Bestenliste', 'club_y': 'Verein in Startrecht'}, inplace=True)

cols = list(data.columns.values)
cols.pop(cols.index('Verein in Bestenliste'))
cols.pop(cols.index('Verein in Startrecht'))
data = data[cols+['Verein in Bestenliste', 'Verein in Startrecht']]

if year == 2023:
    data = data[~((data['firstname'] == 'David') & (data['lastname'] == 'Zeller'))]

print(data)