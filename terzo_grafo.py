import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from matplotlib.patches import Patch
from matplotlib.lines import Line2D



df = pd.read_csv("merged_squadre_ita.csv")
df_squadre = df.team2
df.loc[df['player_age']<=18, 'age'] = 'età 15-18'
df.loc[df['player_age'].between(19,24), 'age'] = 'età 19-25'
df.loc[df['player_age'].between(25,28), 'age'] = 'età 25-28'
df.loc[df['player_age'].between(29,33), 'age'] = 'età 29-33'
df.loc[df['player_age'].between(34,36), 'age'] = '34-40'
df = df.dropna()

G = nx.from_pandas_edgelist(df, "team2", "age", create_using=nx.MultiGraph)
G2 = nx.from_pandas_edgelist(df, "team2", "player_nation", create_using=nx.MultiGraph)
#G3 = nx.from_pandas_edgelist(df, "team2", "league_team1", create_using=nx.MultiGraph)
#G_G2 = nx.compose(G, G2)
B = nx.compose(G, G2)

print("Number of nodes:", B.number_of_nodes())
print("Number of edges:", B.number_of_edges())

# nodes = B.nodes
# for node in nodes:
#     if node == 'nan':
#         B.remove_node(node)

print('Nodes: ', B.nodes)

edgelist = B.edges
print(edgelist)
dict_edges_occurences = {}

for edge in edgelist:
    if (edge[0], edge[1]) not in dict_edges_occurences:
        dict_edges_occurences[(edge[0], edge[1])] = 1
    else:
        dict_edges_occurences[(edge[0], edge[1])] += 1

color_map = []
team_list = df.team2.to_list()
nation_list = df.player_nation.to_list()
for node in B.nodes:
    if node in team_list:
        color_map.append('blue')
    elif node in nation_list:
        color_map.append('green')
    else:
        color_map.append('red')


# size_map = []
# for i in G.nodes:
#     if node in team_list:
#         size_map.append(50)
#     else:
#         size_map.append(20)


legend_elements1 = [Line2D([0], [0], marker='o', color='w', label='team',markerfacecolor='firebrick', markersize=13),
                   Line2D([0], [0], marker='o', color='w', label='eta',markerfacecolor='royalblue', markersize=13)]

pos = nx.spring_layout(B)

# nx.draw_networkx( G,
#         node_color=color_map,
#         node_size=size_map,
#         pos=pos,
#         with_labels=True,
#         )
nx.draw_networkx_nodes(B,pos,
                       nodelist=B.nodes,
                       node_color=color_map,
                       node_size= 40,
                       alpha=0.7)
nx.draw_networkx_edges(B,
                       pos=pos,
                       edgelist = dict_edges_occurences.keys(),
                       width=list(dict_edges_occurences.values()),
                       edge_color='lightgray',
                       alpha=0.6)
nx.draw_networkx_labels(B, pos=pos,
                        labels=dict(zip(B.nodes,B.nodes)),
                        font_color='black',
                        font_size=7)

plt.show()

