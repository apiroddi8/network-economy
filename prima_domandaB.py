import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np


df = pd.read_csv("Dataset/dataset_pulitoCUT07-21.csv")
df = df.dropna()
df_serie = pd.read_csv("Dataset/dataset_supportoCUT.csv")

print(df['market_value'])
df = df.astype({'market_value': float },errors='raise')

df_filtered = df[(df['country_team1'] == 'Italy') & (df['country_team2'] == 'Italy')]
df_filtered = df_filtered[df_filtered['market_value'] >= 20000000.0 ] #da settare a 20mln, 25mln, 30mln
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
fig.suptitle("Football transfers between italian clubs from 2007 to 2021 with filtered market value")

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

#TOP 5 OUT-DEGREE NODES

out_degrees=G.out_degree
out_degrees_dict = {}

for t in out_degrees:
    out_degrees_dict[t[0]] = t[1]

out_degrees_list = sorted(out_degrees_dict.items(), key=lambda x: x[1], reverse=True)
top5_out_degree_nodes = out_degrees_list[:5]

print(top5_out_degree_nodes)

data = top5_out_degree_nodes

plt.bar(*zip(*data), color=sns.color_palette("ch:2,r=.9,l=.6"))

plt.title('Top 5 out degree nodes')

plt.xlabel('Squadre')

plt.ylabel('Out_degree')

plt.xticks(rotation=15)

plt.show()







