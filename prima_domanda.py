# 1)Tenendo conto di una soglia minima di valore del giocatore al momento del
# trasferimento, quali sono le squadre che nel campionato italiano
# più vengono coinvolte nella circolazione in entrata dei calciatori?

# Esiste una tendenza da parte della cerchia ristretta di top club a depredare
# le squadre di fasce più basse all’interno del medesimo campionato,
# è possibile individuare un accentramento di tutti gli acquisti rilevanti
# verso queste squadre? Quante sono? [confronto con altri paesi]

#NODI = squadre
#ARCHI = valore trasferimento esclusa soglia minima

#MEGLIO UTILIZZARE IL MARKET VALUE CHE E' PIù OGGETTIVO, MENTRE IL TRANSFER_VALUE E' PIù SOGGETTO A VARIAZIONI NEL CORSO DEL TEMPO
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import re

df = pd.read_csv("dataset/nostro_df_pulito.csv")
df_clean = df.dropna()
#print(df.columns.tolist())

#Indagare sui quartili della colonna market_value in modo da utilizzare poi nella costruizione del grafico solo dal 1 quartile in su

df_clean = df_clean.astype({'market_value': str },errors='raise')
#print(df_clean['market_value'].str.contains('-').sum())
df_clean = df_clean[df_clean['market_value'].str.contains('-')==False]
#print(df_clean['market_value'])

#convert mln e mila to number
#print(df_clean['market_value'].str.contains('\n       ').sum())

for row in df_clean['market_value']:
    if 'mln €' in row:
        row.replace('mln €', '000000')



print(df_clean['market_value'])




df_clean = df_clean[df_clean['market_value'].str.replace('mila €', '000')]
#print(df_clean['market_value'])


