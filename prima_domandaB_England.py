
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np


df = pd.read_csv("Dataset/dataset_pulitoCUT07-21.csv")
df = df.dropna()
df_serie = pd.read_csv("Dataset/dataset_supportoCUT.csv")

print(df['market_value'])
df = df.astype({'market_value': float },errors='raise')

df_filtered = df[(df['country_team1'] == 'England') & (df['country_team2'] == 'England')]
df_filtered = df_filtered[df_filtered['market_value'] >= 30000000.0 ]    #8000000.0 per fare grafo con poche squadre e milan juve centrali
print(df_filtered)

G=nx.from_pandas_edgelist(df_filtered, "team1", "team2",create_using=nx.MultiDiGraph)
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

print("G.nodes =", G.nodes)
#print("\n\nG.edges =", G.edges)
# print("\n\n\nG.degree =", G.degree)


#COUNTING NUMBER OF EDGES BETWEEN ANY TWO NODES
edgelist = G.edges
dict_edges_occurences = {}

for edge in edgelist:
    if (edge[0], edge[1]) not in dict_edges_occurences:
        dict_edges_occurences[(edge[0], edge[1])] = 1
    dict_edges_occurences[(edge[0], edge[1])] += 1

#print("AAAA",  sorted(dict_edges_occurences.items(), key=lambda x: x[1], reverse=True))


#Visualize the graph
fig, ax = plt.subplots(figsize=(45, 35))
fig.suptitle("football player transfer from 2007 to 2021 with filtered market value")

size_map = []
in_degrees = G.in_degree
for i in G.nodes:
    for node in in_degrees:
        if node[0] == i:
            in_degree = node[1]
    size_map.append(in_degree * 30)


pos = nx.kamada_kawai_layout(G)

nx.draw_networkx_nodes(G,pos,
                       nodelist=G.nodes,
                       node_size=size_map,
                       node_color='blue',
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
                        font_size=6)

plt.axis('off')
plt.show()








