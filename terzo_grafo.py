import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from matplotlib.patches import Patch
from matplotlib.lines import Line2D



dataframe = pd.read_csv("merged_squadre_ita.csv")

df = dataframe[dataframe['country_team2'] == 'Italy']

df.loc[df['player_age']<=18, 'age'] = 'età 15-18'
df.loc[df['player_age'].between(19,24), 'age'] = 'età 19-25'
df.loc[df['player_age'].between(25,28), 'age'] = 'età 25-28'
df.loc[df['player_age'].between(29,33), 'age'] = 'età 29-33'
df.loc[df['player_age'].between(34,36), 'age'] = '34-40'
df = df.dropna()

df_filtered = df[(df['market_value'] != 'NF') & (df['market_value'] != '-')]
df_filtered = df_filtered.astype({'market_value': float },errors='raise')

first_quartile_market_value = df_filtered['market_value'].quantile(q=0.25)
second_quartile_market_value = df_filtered['market_value'].quantile(q=0.5)


df_filtered.loc[df_filtered['market_value'] <= first_quartile_market_value, 'market_value_cat'] = 'low_value'
df_filtered.loc[(df_filtered['market_value'] <= second_quartile_market_value) & (df_filtered['market_value'] > first_quartile_market_value), 'market_value_cat'] = 'medium_value'
df_filtered.loc[df_filtered['market_value'] > second_quartile_market_value, 'market_value_cat'] = 'high_value'
df_filtered = df_filtered.dropna()


G = nx.from_pandas_edgelist(df_filtered, "team2", "age", create_using=nx.MultiGraph)
G2 = nx.from_pandas_edgelist(df_filtered, "team2", "league_team1", create_using=nx.MultiGraph)
# GROUP BY LEAGUE_TEAM WITH ONLY ONE EDGE
edgelist = G2.edges
dict_edges_occurences = {}

for edge in edgelist:
    if (edge[0], edge[1]) not in dict_edges_occurences:
        dict_edges_occurences[(edge[0], edge[1])] = 1
    else:
        dict_edges_occurences[(edge[0], edge[1])] += 1

print(dict_edges_occurences)
team_list = df.team2.to_list()
edge_only1 = []
for k,v in dict_edges_occurences.items():
    if v == 1:
        edge_only1.append(k)

nation2group = []
for t in edge_only1:
    for e in t:
        if e not in team_list:
            nation2group.append(e)

nation2group = set(nation2group)
print(nation2group)

#G3 = nx.from_pandas_edgelist(df_filtered, "team2", "player_nation", create_using=nx.MultiGraph)
# G4 = nx.from_pandas_edgelist(df_filtered, "team2", "market_value_cat", create_using=nx.MultiGraph)
# G_G2 = nx.compose(G, G2)
# G_G2_G3 = nx.compose(G_G2, G3)
# B = nx.compose(G_G2_G3, G4)

# print("Number of nodes:", B.number_of_nodes())
# print("Number of edges:", B.number_of_edges())
#print('Nodes: ', B.nodes)

# edgelist = B.edges
# dict_edges_occurences = {}
#
# for edge in edgelist:
#     if (edge[0], edge[1]) not in dict_edges_occurences:
#         if edge[1] == 'Italy':
#             dict_edges_occurences[(edge[0], edge[1])] = 0.1
#         else:
#             dict_edges_occurences[(edge[0], edge[1])] = 1
#     else:
#         if edge[1] == 'Italy':
#             dict_edges_occurences[(edge[0], edge[1])] += 0.1
#         else:
#             dict_edges_occurences[(edge[0], edge[1])] += 1



#
# color_map = []
# league_list = df.league_team1.to_list()
# nation_list = df.player_nation.to_list()
# market_value_list = ['low_value', 'medium_value', 'high_value']
# for node in B.nodes:
#     if node in team_list:
#         color_map.append('blue')
#     elif node in league_list:
#         color_map.append('green')
#     elif node in market_value_list:
#         color_map.append('yellow')
#     else:
#         color_map.append('red')
#
#
# # size_map = []
# # for i in G.nodes:
# #     if node in team_list:
# #         size_map.append(50)
# #     else:
# #         size_map.append(20)
#
#
# legend_elements1 = [Line2D([0], [0], marker='o', color='w', label='team',markerfacecolor='firebrick', markersize=13),
#                    Line2D([0], [0], marker='o', color='w', label='eta',markerfacecolor='royalblue', markersize=13)]
#
# pos = nx.spring_layout(B)
#
# nx.draw_networkx_nodes(B,pos,
#                        nodelist=B.nodes,
#                        node_color=color_map,
#                        node_size= 40,
#                        alpha=0.7)
# nx.draw_networkx_edges(B,
#                        pos=pos,
#                        edgelist = dict_edges_occurences.keys(),
#                        width=list(dict_edges_occurences.values()),
#                        edge_color='lightgray',
#                        alpha=0.6)
# nx.draw_networkx_labels(B, pos=pos,
#                         labels=dict(zip(B.nodes,B.nodes)),
#                         font_color='black',
#                         font_size=7)
#
# plt.show()
