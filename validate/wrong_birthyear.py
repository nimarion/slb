import pandas as pd

year = 2023

athletes = pd.read_csv('validate/' + str(year) + '/athletes.csv')
data = pd.read_csv('data/' + str(year) + '.csv')

data = data.merge(athletes, left_on=['firstname', 'lastname', 'club'], right_on=['firstname', 'lastname', 'club'])
data = data[data['birthyear_x'] != data['birthyear_y']]
data = data[data.apply(lambda row: row['ageGroup'][0].replace('F', 'W') == row['sex'], axis=1)]
data.drop(columns=['athleteId', 'sex', 'country', 'result', 'location', 'teamResult', 'place'], inplace=True)
data.rename(columns={'birthyear_x': 'Jahrgang in Bestenliste', 'birthyear_y': 'Jahrgang in Startrecht'}, inplace=True)

cols = list(data.columns.values)
cols.pop(cols.index('Jahrgang in Bestenliste'))
cols.pop(cols.index('Jahrgang in Startrecht'))
data = data[cols+['Jahrgang in Bestenliste', 'Jahrgang in Startrecht']]

data.to_excel('tmp/wrong_birthyear_' + str(year) + '.xlsx', index=False)

print(data)