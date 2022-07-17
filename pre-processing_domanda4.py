import pandas as pd


#join di due dataframe per la creazione delle fasce
df = pd.read_csv("dataset//dataset_pulitoCUT07-21.csv")
df= df[(df['season']>2009)&(df['season']<2020)]
df1 = pd.read_csv("squadre_per_fascia//squadre_ita_eterne.csv")
lista = list(df1.team)
df2 = df[df['team2'].isin(lista)].copy()
df2.sort_values(['team2','season'], ascending=[True, True], inplace=True)
df2.to_csv("Dataset//merged_squadre_ita.csv")



