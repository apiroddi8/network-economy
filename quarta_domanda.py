import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from matplotlib.patches import Patch
from matplotlib.lines import Line2D



dataframe = pd.read_csv("Dataset//merged_squadre_ita.csv")
df_ita_eterne = pd.read_csv("squadre_per_fascia/squadre_ita_eterne.csv")

df = dataframe[dataframe['country_team2'] == 'Italy']

df.loc[df['player_age']<=22, 'age'] = '17-22'
df.loc[df['player_age'].between(23,28), 'age'] = '23-28'
df.loc[df['player_age'].between(29,34), 'age'] = '29-34'
df.loc[df['player_age'].between(35,40), 'age'] = '35-40'
df = df.dropna()

df_filtered = df[(df['market_value'] != 'NF') & (df['market_value'] != '-')]
df_filtered = df_filtered.astype({'market_value': float },errors='raise')


df_filtered.loc[df_filtered['market_value'] <= 8000000.0, 'market_value_cat'] = 'low_value'
df_filtered.loc[(df_filtered['market_value'] <= 16000000.0) & (df_filtered['market_value'] > 8000000.0), 'market_value_cat'] = 'medium_value'
df_filtered.loc[(df_filtered['market_value'] <= 24000000.0) & (df_filtered['market_value'] > 16000000.0), 'market_value_cat'] = 'high_value'
df_filtered.loc[df_filtered['market_value'] > 24000000.0, 'market_value_cat'] = 'top_value'
df_filtered = df_filtered.dropna()

top_EU_leagues=['ENG1','SPA1','GER1','POR1','FRA1']
top_SA_leagues=['ARG','BRA','URU']
EU_leagues=['NET1','BEL','CRO','GRE','RUS','ENG2','SWI','ROM','SPA2','SWE','FRA2','SER','DEN','TUR','UKR','CZE','SLO','POL','UNI','HUN']
SA_leagues=['CHI','COL','PAR','VEN','BOL','PER']

df_filtered.loc[df_filtered['league_team1'].isin(top_EU_leagues),'league_team1']='TOP EU'
df_filtered.loc[df_filtered['league_team1'].isin(top_SA_leagues),'league_team1']='TOP SA'
df_filtered.loc[df_filtered['league_team1'].isin(EU_leagues),'league_team1']='LOW EU'
df_filtered.loc[df_filtered['league_team1'].isin(SA_leagues),'league_team1']='LOW SA'
df_filtered.loc[(df_filtered['league_team1']!='TOP EU')&(df_filtered['league_team1']!='TOP SA')&(df_filtered['league_team1']!='LOW EU')&(df_filtered['league_team1']!='LOW SA'),'league_team1']='OTH'


G = nx.from_pandas_edgelist(df_filtered, "team2", "age", edge_attr= 'age',create_using=nx.MultiGraph)
G2 = nx.from_pandas_edgelist(df_filtered, "team2", "league_team1", edge_attr= 'league_team1',create_using=nx.MultiGraph)
G4 = nx.from_pandas_edgelist(df_filtered, "team2", "market_value_cat", edge_attr= 'market_value_cat' ,create_using=nx.MultiGraph)
G_G2 = nx.compose(G, G2)
B=nx.compose(G_G2,G4)

print("Number of nodes:", B.number_of_nodes())
print("Number of edges:", B.number_of_edges())
print('Nodes: ', B.nodes)

edgelist = B.edges
dict_edges_occurences = {}

for edge in edgelist:
    if (edge[0], edge[1]) not in dict_edges_occurences:
        if edge[1] == 'Italy':
            dict_edges_occurences[(edge[0], edge[1])] = 0.1
        else:
            dict_edges_occurences[(edge[0], edge[1])] = 1
    else:
        if edge[1] == 'Italy':
            dict_edges_occurences[(edge[0], edge[1])] += 0.1
        else:
            dict_edges_occurences[(edge[0], edge[1])] += 1

print(dict_edges_occurences)


color_map = []
team_list = df_filtered.team2.tolist()
team_levelTOP = ['Juventus FC','FC Inter','AS Roma','AC Milan','SSC Napoli','SS Lazio', 'UC Sampdoria']
team_levelMEDIUM = ['Genoa CFC','Cagliari Calcio', 'Torino FC', 'Bologna FC 1909', 'Chievo Verona', 'Palermo', 'Parma']
team_levelLOW = ['Delfino Pescara 1936', 'Novara Calcio 1908', 'Salernitana', 'Ascoli Calcio 1898', 'Venezia', 'ACR Messina']
league_list = df_filtered.league_team1.tolist()
age_list = df_filtered.age.unique().tolist()
market_value_list = ['low_value', 'medium_value', 'high_value', 'top_value']
for node in B.nodes:
    if node in team_levelTOP:
        color_map.append('blue')
    elif node in team_levelMEDIUM:
        color_map.append('cyan')
    elif node in team_levelLOW:
        color_map.append('dodgerblue')
    elif node in league_list:
        color_map.append('green')
    elif node in market_value_list:
        color_map.append('yellow')
    else:
        color_map.append('orange')


legend_elements1 = [Line2D([0], [0], marker='o', color='w', label='Serie A - TOP ',markerfacecolor='blue', markersize=13),
                    Line2D([0], [0], marker='o', color='w', label='Serie A - MEDIUM',markerfacecolor='cyan', markersize=13),
                    Line2D([0], [0], marker='o', color='w', label='Serie A - LOW',markerfacecolor='dodgerblue', markersize=13),
                    Line2D([0], [0], marker='o', color='w', label='League',markerfacecolor='green', markersize=13),
                    Line2D([0], [0], marker='o', color='w', label='Market value',markerfacecolor='yellow', markersize=13),
                    Line2D([0], [0], marker='o', color='w', label='Age',markerfacecolor='orange', markersize=13)]


pos = nx.kamada_kawai_layout(B)
fig, ax = plt.subplots(figsize=(40, 35))
nx.draw_networkx_nodes(B,pos,
                       nodelist=B.nodes,
                       node_color=color_map,
                       node_size= 90,
                       alpha=0.7)
nx.draw_networkx_edges(B,
                       pos=pos,
                       edgelist = dict_edges_occurences.keys(),
                       width=list(i / 15 for i in dict_edges_occurences.values()),
                       edge_color='lightgray',
                       alpha=0.6)
nx.draw_networkx_labels(B, pos=pos,
                        labels=dict(zip(B.nodes,B.nodes)),
                        font_color='black',
                        font_size=7)

ax.legend(handles=legend_elements1, loc='lower right', prop={'size': 10})
plt.show()
