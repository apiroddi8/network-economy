import pandas as pd
# df = pd.read_csv("dataset//dataset_finale10_15pronto.csv")
# df1 = df[df.league_team1.str.startswith("ITA")]
#
# df_filter = df1.groupby(['team1','league_team1'])['season'].unique().apply(list).reset_index()
# data = pd.DataFrame(data=df_filter)
# data.to_csv("df_squadre.csv", index=False)
#
# nuovo_df = pd.read_csv("df_squadre.csv")
# df_filter2 = nuovo_df.groupby(['team1','league_team1'])["season"].agg(lambda x: x.str.len().max()).reset_index()
# df_sorted = df_filter2.sort_values(by="season")
# nuovo_data = pd.DataFrame(data=df_sorted)
# nuovo_data.to_csv("squadre_ordinate.csv")
# print(df_filter2)

#join di due dataframe per la creazione delle fasce
df = pd.read_csv("dataset//dataset_completo10-15.csv")
df1 = pd.read_csv("squadre_per_fascia//squadre_ita_eterne.csv")
lista = list(df1.team)
df2 = df[df['team2'].isin(lista)].copy()
df2.sort_values(['team2','season'], ascending=[True, True], inplace=True)
df2.to_csv("merged_squadre_ita.csv")


#creazione fasce di età
# df.loc[df['player_age']<=18, 'age'] = 'età 15-18'
# df.loc[df['player_age'].between(19,24), 'age'] = 'età 19-25'
# df.loc[df['player_age'].between(25,28), 'age'] = 'età 25-28'
# df.loc[df['player_age'].between(29,33), 'age'] = 'età 29-33'
# df.loc[df['player_age'].between(34,36), 'age'] = 'vecchio'
#
# print(df.age)

# import pandas as pd
# df=pd.read_csv('Dataset/dataset_completo10-15.csv')
# new_df=df.groupby('player_name').first().reset_index()
# new_df2=new_df[new_df['league_team1']=='ITAJ']
# player_list=new_df2['player_name'].tolist()
# dataframe=df[df['player_name'].isin(player_list)]
# new_dataframe=dataframe[dataframe['league_team2']=='ITA1']
# player_list2=list(set(new_dataframe['player_name'].tolist()))
#
# data=dataframe[dataframe['player_name'].isin(player_list2)]
# esclusi=[]
# print(data)
# print(len(data.index))
# righe=list(range(0,len((data.index))))
# print(righe)
# data['indice']=righe
# print(data)
# for player in player_list2:
#     for row in data.itertuples():
#         if row.player_name==player:
#             for row2 in data.itertuples():
#                 if ((row2.season == row.season or row2.season==row.season+1) and row2.league_team2!='ITA1' and row2.player_name==player and row2.indice!=row.indice):
#                     esclusi.append(player)
#
# data2=data[~data['player_name'].isin(esclusi)]
#
# for index,row in data2.iterrows():
#     if row.league_team2=='ITA1':
#         for index2,row2 in data2.iterrows():
#             if (row2.player_name==row.player_name and row2.indice>row.indice):
#                 data2.drop(index2, inplace=True)
#
#
# #df_filter = df.groupby(['team1','team2'])['player_name'].unique().apply(dict).reset_index()
#
# new_dict = (data2.groupby('player_name').apply(lambda x: list(map(tuple, zip(x['team1'],x['team2'])))).to_dict())
# print(new_dict)
#
#
