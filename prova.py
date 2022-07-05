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

df = pd.read_csv("dataset_finale11-15pronto.csv")
df1 = pd.read_csv("squadre_per_fascia//low_league.csv")
merged_Frame = pd.merge(df, df1, how='inner', left_on='team1', right_on='team')
merged_Frame.drop('league', inplace=True, axis=1)
merged_Frame.drop('team', inplace=True, axis=1)
merged_Frame.drop('point', inplace=True, axis=1)
merged_Frame.to_csv("merged_low_league.csv")



