import pandas as pd
df = pd.read_csv("dataset//dataset_finale10_15pronto.csv")
df1 = df[df.league_team1.str.startswith("ITA")]

df_filter = df1.groupby(['team1','league_team1'])['season'].unique().apply(list).reset_index()
data = pd.DataFrame(data=df_filter)
data.to_csv("df_squadre.csv", index=False)

nuovo_df = pd.read_csv("df_squadre.csv")
df_filter2 = nuovo_df.groupby(['team1','league_team1'])["season"].agg(lambda x: x.str.len().max()).reset_index()
df_sorted = df_filter2.sort_values(by="season")
nuovo_data = pd.DataFrame(data=df_sorted)
nuovo_data.to_csv("squadre_ordinate.csv")
print(df_filter2)




