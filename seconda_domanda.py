import pandas as pd
df=pd.read_csv('Dataset/dataset_completo10-15.csv')
new_df=df.groupby('player_name').first().reset_index()
print(new_df)
new_df2=new_df[new_df['league_team1']=='ITA4']
print(new_df2)
player_list=new_df2['player_name'].tolist()
dataframe=df[df['player_name'].isin(player_list)]
print(dataframe)
new_dataframe=dataframe[dataframe['league_team2']=='ITA1']
player_list2=list(set(new_dataframe['player_name'].tolist()))
print(player_list2)

data=dataframe[dataframe['player_name'].isin(player_list2)]
esclusi=[]
salvati=[]
print(data)
print(len(data.index))
righe=list(range(0,len((data.index))))
print(righe)
data['indice']=righe
print(data)
print(player_list)
for player in player_list2:
    for row in data.itertuples():
        if row.player_name==player:
            for row2 in data.itertuples():
                if ((row2.season == row.season or row2.season==row.season+1) and row2.league_team2!='ITA1' and row2.player_name==player and row2.indice!=row.indice):
                    for row3 in data.itertuples():
                        if (row3.indice!=row2.indice and row3.indice!=row.indice and row3.league_team2=='ITA1' and row3.player_name==player):
                            #esclusi.append(player)
                            salvati.append(player)
                    if player not in salvati:
                        esclusi.append(player)

print(esclusi)
data2=data[~data['player_name'].isin(esclusi)]


bandiere=[]
for raw in data2.itertuples():
    check=True
    if raw.league_team2=='ITA1':
        for raw2 in data2.itertuples():
            if (raw2.indice > raw.indice and (raw2.season==raw.season or raw2.season==raw.season+1) and raw2.league_team2!='ITA1' and raw2.player_name==raw.player_name):
                bandiere.append('red')
                check=False
                break
        if check:
            bandiere.append('green')

    else:
        bandiere.append('red')

print(len(bandiere))
data2['bandiere']=bandiere

print(data2)

data2 = data2.astype({'indice': int },errors='raise')

player_list3 = data2.player_name.unique().tolist()
indice = {}
for player in player_list3:
    for row in data2.itertuples():
            if row.bandiere == 'green' and row.player_name == player:
                indice[player] = row.indice


print(indice)
print(data2)
for index, row in data2.iterrows():
    for player, ind in indice.items():
        if row.indice < ind and row.player_name == player:
            data2.at[index,'bandiere'] = 'green'

data2 = data2[(data2['bandiere'] == 'green')]

print('dopo modifica bandiera\n',data2)

new_dict = (data2.groupby('player_name').apply(lambda x: list(map(tuple, zip(x['team1'],x['team2'])))).to_dict())
print(new_dict)
print(len(new_dict))
print(new_dict.keys())





