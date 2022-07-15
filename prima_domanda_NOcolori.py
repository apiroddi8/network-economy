from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import seaborn as sns


df = pd.read_csv("Dataset/dataset_pulitoCUT07-21.csv")
df = df.dropna()
df_serie = pd.read_csv("Dataset/dataset_supportoCUT.csv")


print(df['market_value'])
df = df.astype({'market_value': float },errors='raise')
first_quartile_market_value = df['market_value'].quantile(q=0.25)
print(first_quartile_market_value)

df_filtered = df[(df['country_team1'] == 'Italy') & (df['country_team2'] == 'Italy')]
df_filtered = df_filtered[df_filtered['market_value'] >= first_quartile_market_value ]
print(df_filtered)

G=nx.from_pandas_edgelist(df_filtered, "team1", "team2",create_using=nx.MultiDiGraph)
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

print("G.nodes =", G.nodes)
#print("\n\nG.edges =", G.edges)
#print("\n\n\nG.degree =", G.degree)

# CHECK NODES MISSING IN STEP4.csv
missing_teams = []
teams = df_serie.team1.tolist()
for node in G.nodes:
     if node not in teams:
         missing_teams.append(node)

for node in missing_teams:
    G.remove_node(node)

#BETWEENESS
bw_centrality = nx.betweenness_centrality(G, normalized=False)
#print("\n\nBetweenness Centrality: ", sorted(bw_centrality.items(), key=lambda x: x[1], reverse=True))
bw_value = [value for value in bw_centrality.values()]
quantiles = np.quantile(bw_value, [0.25, 0.5, 0.75])


#COUNTING NUMBER OF EDGES BETWEEN ANY TWO NODES
edgelist = G.edges
dict_edges_occurences = {}

for edge in edgelist:
    if (edge[0], edge[1]) not in dict_edges_occurences:
        dict_edges_occurences[(edge[0], edge[1])] = 1
    dict_edges_occurences[(edge[0], edge[1])] += 1

print("AAAA",  sorted(dict_edges_occurences.items(), key=lambda x: x[1], reverse=True))


#Visualize the graph
fig, ax = plt.subplots(figsize=(45, 35))
fig.suptitle("football player transfer from 2007 to 2021")

size_map = []
degrees = G.degree
for i in G.nodes:
    for node in degrees:
        if node[0] == i:
            degree = node[1]
    size_map.append(degree * 15 )


pos = nx.kamada_kawai_layout(G)
nx.draw_networkx_nodes(G,pos,
                       nodelist=G.nodes,
                       node_size=size_map,
                       node_color='lightblue',
                       alpha=0.7)
nx.draw_networkx_edges(G,
                       pos=pos,
                       edgelist = dict_edges_occurences.keys(),
                       width=list(dict_edges_occurences.values()),
                       edge_color='lightgray',
                       alpha=0.6)
nx.draw_networkx_labels(G, pos=pos,
                        labels=dict(zip(G.nodes,G.nodes)),
                        font_color='black',
                        font_size=5)


plt.axis('off')
plt.show()