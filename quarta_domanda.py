import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from matplotlib.patches import Patch
from matplotlib.lines import Line2D



dataframe = pd.read_csv("merged_squadre_ita.csv")

df = dataframe[dataframe['country_team2'] == 'Italy']

df.loc[df['player_age']<=22, 'age'] = '17-22'
df.loc[df['player_age'].between(23,28), 'age'] = '23-28'
df.loc[df['player_age'].between(29,34), 'age'] = '29-34'
df.loc[df['player_age'].between(35,40), 'age'] = '35-40'
df = df.dropna()

df_filtered = df[(df['market_value'] != 'NF') & (df['market_value'] != '-')]
df_filtered = df_filtered.astype({'market_value': float },errors='raise')

# first_quartile_market_value = df_filtered['market_value'].quantile(q=0.25)
# second_quartile_market_value = df_filtered['market_value'].quantile(q=0.5)
# print('QUARTILI: ', first_quartile_market_value, second_quartile_market_value)

df_filtered.loc[df_filtered['market_value'] <= 8000000.0, 'market_value_cat'] = 'low_value'
df_filtered.loc[(df_filtered['market_value'] <= 16000000.0) & (df_filtered['market_value'] > 8000000.0), 'market_value_cat'] = 'medium_value'
df_filtered.loc[(df_filtered['market_value'] <= 24000000.0) & (df_filtered['market_value'] > 16000000.0), 'market_value_cat'] = 'high_value'
df_filtered.loc[df_filtered['market_value'] > 24000000.0, 'market_value_cat'] = 'top_value'
df_filtered = df_filtered.dropna()

league_counts = df['league_team1'].value_counts().to_dict()
print("\n\nLeagues count: ", sorted(league_counts.items(), key=lambda x: x[1], reverse=True))
print(len([key for key in league_counts.keys()]))
print(len([value for value in league_counts.values() if value > 7]))
#get first 20th league except italia
first_20th = [key for key, value in league_counts.items() if value > 7]
print(first_20th)

df_filtered.loc[(~df_filtered['league_team1'].isin(first_20th)), 'league_team1'] = 'OTHER'

nation_counts = df['player_nation'].value_counts().to_dict()
print("\n\nLeagues count: ", sorted(nation_counts.items(), key=lambda x: x[1], reverse=True))
print(len([key for key in nation_counts.keys()]))
print(len([value for value in nation_counts.values() if value >= 15]))
# get first 25th nation
first_25th = [key for key, value in nation_counts.items() if value >= 15]
print(first_25th)

df_filtered.loc[(~df_filtered['player_nation'].isin(first_25th)), 'player_nation'] = 'Other_nation'


G = nx.from_pandas_edgelist(df_filtered, "team2", "age", edge_attr= 'age',create_using=nx.MultiGraph)
G2 = nx.from_pandas_edgelist(df_filtered, "team2", "league_team1", edge_attr= 'league_team1',create_using=nx.MultiGraph)
G3 = nx.from_pandas_edgelist(df_filtered, "team2", "player_nation", edge_attr= 'player_nation',create_using=nx.MultiGraph)
G4 = nx.from_pandas_edgelist(df_filtered, "team2", "market_value_cat", edge_attr= 'market_value_cat' ,create_using=nx.MultiGraph)
G_G2 = nx.compose(G, G2)
G_G2_G3 = nx.compose(G_G2, G3)
B = nx.compose(G_G2_G3, G4)

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
league_list = df_filtered.league_team1.tolist()
nation_list = df_filtered.player_nation.tolist()
age_list = df_filtered.age.unique().tolist()
market_value_list = ['low_value', 'medium_value', 'high_value', 'top_value']
for node in B.nodes:
    if node in team_list:
        color_map.append('blue')
    elif node in league_list:
        color_map.append('green')
    elif node in market_value_list:
        color_map.append('yellow')
    elif node in age_list:
        color_map.append('orange')
    else:
        color_map.append('red')

# #CREATE DATAFRAME FOR MAX E MIN AGE FOR TEAM
# new_df=df_filtered.groupby(['team2', 'age']).size().reset_index()
# new_df.to_csv("valori_eta.csv")
# dfcv = pd.read_csv("valori_eta.csv")
# dfc= dfcv.sort_values(by="0")
# val_eta_max = dfc.drop_duplicates(subset='team2', keep="last")
# val_eta_max.to_csv('prov.csv')
# val_eta_min=dfc.drop_duplicates(subset='team2', keep="first")
#
# color_edge_map = []
# edge_age = []
# edge_age2 = {}
# for node1, node2, data in G.edges.data():
#     if data['age']:
#         edge_age.append((node1, node2))
#
# print(edge_age)
#
# for edge, v in dict_edges_occurences:
#         if edge in edge_age:
#             edge_age2[edge] = v
#
# print(edge_age2)
#
# for row in val_eta_max.itertuples():
#     for edge, v in edge_age2:
#         print(row.team2)
# #         if edge == (row.team2, row.age):
# #             color_edge_map.append('red')
# #
# # for row in val_eta_min.itertuples():
# #     for edge, v in edge_age2:
# #         if edge == (row.team2, row.age):
# #             color_edge_map.append('blue')
# #
# # print(color_edge_map)
#
legend_elements1 = [Line2D([0], [0], marker='o', color='w', label='team',markerfacecolor='firebrick', markersize=13),
                   Line2D([0], [0], marker='o', color='w', label='eta',markerfacecolor='royalblue', markersize=13)]

pos = nx.kamada_kawai_layout(B)
fig, ax = plt.subplots(figsize=(40, 35))
nx.draw_networkx_nodes(B,pos,
                       nodelist=B.nodes,
                       node_color=color_map,
                       node_size= 40,
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
ax.legend(handles=legend_elements1, loc='lower left', prop={'size': 12})
plt.show()
