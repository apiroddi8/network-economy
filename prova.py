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
# df = pd.read_csv("dataset//dataset_finale11-15pronto.csv")
# df1 = pd.read_csv("squadre_per_fascia//top_leagues.csv")
# merged_Frame = pd.merge(df, df1, how='inner', left_on='team2', right_on='team')
# merged_Frame.drop('league', inplace=True, axis=1)
# merged_Frame.drop('team', inplace=True, axis=1)
# merged_Frame.drop('point', inplace=True, axis=1)
# merged_Frame.to_csv("merged_top_league.csv")


#creazione fasce di età
# df.loc[df['player_age']<=18, 'age'] = 'età 15-18'
# df.loc[df['player_age'].between(19,24), 'age'] = 'età 19-25'
# df.loc[df['player_age'].between(25,28), 'age'] = 'età 25-28'
# df.loc[df['player_age'].between(29,33), 'age'] = 'età 29-33'
# df.loc[df['player_age'].between(34,36), 'age'] = 'vecchio'
#
# print(df.age)

