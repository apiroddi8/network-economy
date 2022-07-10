import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
df = pd.read_csv("merged_squadre_ita.csv")
df_squadre = df.team2
df.loc[df['player_age']<=18, 'age'] = 'età 15-18'
df.loc[df['player_age'].between(19,24), 'age'] = 'età 19-25'
df.loc[df['player_age'].between(25,28), 'age'] = 'età 25-28'
df.loc[df['player_age'].between(29,33), 'age'] = 'età 29-33'
df.loc[df['player_age'].between(34,36), 'age'] = '34-40'
df.age = df.age.dropna()
df.team2 = df.team2.dropna()
B = nx.from_pandas_edgelist(df, "team2", "age",create_using=nx.Graph)
print("Number of nodes:", B.number_of_nodes())
print("Number of edges:", B.number_of_edges())

edgelist = B.edges
dict_edges_occurences = {}

for edge in edgelist:
    if (edge[0], edge[1]) not in dict_edges_occurences:
        dict_edges_occurences[(edge[0], edge[1])] = 1
    dict_edges_occurences[(edge[0], edge[1])] += 1
color_map = []
for node in B.nodes:
    if node in df.team2:
        color_map.append('blue')
    elif node in df.age:
        color_map.append('red')



from matplotlib.patches import Patch
from matplotlib.lines import Line2D

legend_elements1 = [Line2D([0], [0], marker='o', color='w', label='team',markerfacecolor='firebrick', markersize=13),
                   Line2D([0], [0], marker='o', color='w', label='eta',markerfacecolor='royalblue', markersize=13)]

pos = nx.kamada_kawai_layout(B)  # questa cosa l'ho presa dal report di Andrea Carta, dicono che i nodi che sono in posizione centrale sono quei nodi che sono maggiormente connessi con tutti gli altri
# #                                         #nodi; mentre quelli nella periferia presentano il mimor numero di connessioni, e la loro distanza media (considerando il sentiero minimale) è alta.
# nx.draw_networkx( G,
#         node_color=color_map,
#         node_size=size_map,
#         pos=pos,
#         with_labels=True,
#         )
nx.draw_networkx_nodes(B,pos,
                       nodelist=B.nodes,
                       node_color=color_map,
                       alpha=0.7)
nx.draw_networkx_edges(B,
                       pos=pos,
                       edgelist = dict_edges_occurences.keys(),
                       width=list(dict_edges_occurences.values()),
                       edge_color='lightgray',
                       alpha=0.6)
nx.draw_networkx_labels(B, pos=pos,
                        labels=dict(zip(B.nodes,B.nodes)),
                        font_color='black')

plt.show()

