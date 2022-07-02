import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import scipy as sp
from matplotlib.cm import ScalarMappable

df = pd.read_csv("dataset_finale_1011_pulito.csv")
df = df.dropna()


df = df[df['market_value'].str.contains('NF')==False]
df = df[df['market_value'].str.contains('-')==False]
print(df['market_value'])
df = df.astype({'market_value': float },errors='raise')
first_quartile_market_value = df['market_value'].quantile(q=0.25)
print(first_quartile_market_value)

df_filtered = df[(df['country_team1'] == 'Italy') & (df['country_team2'] == 'Italy')]
df_filtered = df_filtered[df_filtered['market_value'] >= first_quartile_market_value]
print(df_filtered)
#
G=nx.from_pandas_edgelist(df_filtered, "team1", "team2")
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

print("G.nodes =", G.nodes)
print("\n\nG.edges =", G.edges)
print("\n\n\nG.degree =", G.degree)

#BETWEENESS
bw_centrality = nx.betweenness_centrality(G, normalized=False)
print("\n\nBetweenness Centrality: ", sorted(bw_centrality.items(), key=lambda x: x[1], reverse=True))
bw_value = [value for value in bw_centrality.values()]
quantiles = np.quantile(bw_value, [0.25, 0.5, 0.75])


#DISEGNINO BURDO
# plt.figure(figsize =(15, 15))
# nx.draw_networkx(G, with_labels = True)
# plt.show()


#Visualize the graph
plt.figure("football player transfer from 2009 to 2021")
fig, ax = plt.subplots(figsize=(25, 15))
#Simple 1-line code: nx.draw_networkx(G)
color_map = []
size_map = []
for i in G.nodes:
    size_map.append(bw_centrality[i] + 50)
    if bw_centrality[i] <= quantiles[0]:
        color_map.append('red')
    elif bw_centrality[i] > quantiles[0] and bw_centrality[i] <= quantiles[1]:
        color_map.append('yellow')
    else:
        color_map.append('green')
nx.draw_networkx( G,
        node_color=color_map,
        node_size=size_map,
        pos=nx.kamada_kawai_layout(G),    # questa cosa l'ho presa dal report di Andrea Carta, dicono che i nodi che sono in posizione centrale sono quei nodi che sono maggiormente connessi con tutti gli altri
                                        #nodi; mentre quelli nella periferia presentano il mimor numero di connessioni, e la loro distanza media (considerando il sentiero minimale) è alta.
        arrows=False, with_labels=True,
        edge_color="gainsboro",
        )
plt.show()


#PUNTO B
#CLUSTERING COEFFICIENT Nella teoria dei grafi, il coefficiente di clustering (o transitività) è la misura del grado in cui i nodi di un grafo tendono ad essere connessi fra loro.
#L'evidenza suggerisce che nella maggior parte delle reti del mondo reale, e in particolare nelle reti sociali, i nodi tendono a creare gruppi fortemente uniti e caratterizzati da una densità di collegamenti
#relativamente alta; il coefficiente di clustering delle reti reali tende quindi ad essere maggiore rispetto a quello dei grafi in cui i collegamenti sono generati casualmente.

# lcc = nx.clustering(G)
#
# cmap = plt.get_cmap('autumn')
# norm = plt.Normalize(0, max(lcc.values()))
# node_colors = [cmap(norm(lcc[node])) for node in G.nodes]
#
# fig, ax = plt.subplots( figsize=(25, 20))
# nx.draw_spring(G, node_color=node_colors, with_labels=True, ax=ax, edge_color="gainsboro")
# fig.colorbar(ScalarMappable(cmap=cmap, norm=norm), label='Clustering', shrink=0.95, ax=ax)
#
#
# fig, ax = plt.subplots( figsize=(15, 10))
# ax.hist(lcc.values(), bins=10)
# ax.set_xlabel('Clustering')
# ax.set_ylabel('Frequency')
#
# plt.tight_layout()
# plt.show()