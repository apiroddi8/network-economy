
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
#df_filtered = df_filtered[df_filtered['market_value'] >= first_quartile_market_value ] #da commentare per grafo senza filtro market value
print(df_filtered)

G=nx.from_pandas_edgelist(df_filtered, "team1", "team2",create_using=nx.MultiDiGraph)
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

print("G.nodes =", G.nodes)
#print("\n\nG.edges =", G.edges)
#print("\n\n\nG.degree =", G.degree)

# CHECK NODES MISSING IN dataset_supportoCUT.csv
missing_teams = []
teams = df_serie.team1.tolist()
for node in G.nodes:
     if node not in teams:
         missing_teams.append(node)

for node in missing_teams:
    G.remove_node(node)




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
fig.suptitle("Football transfers between italian clubs from 2007 to 2021")
color_map = []
size_map = []
degrees = G.degree
for i in G.nodes:
    for node in degrees:
        if node[0] == i:
            degree = node[1]
    size_map.append(degree * 7 )
    for row in df_serie.itertuples():
        if row.team1 == i:
            if row.league_team1 == 'ITA1':
                color_map.append('cyan')
            elif row.league_team1 == 'ITA2':
                color_map.append('yellow')
            elif row.league_team1 == 'ITA3':
                color_map.append('green')
            elif row.league_team1 == 'ITA4':
                color_map.append('red')
            else:
                color_map.append('purple')


legend_elements1 = [Line2D([0], [0], marker='o', color='w', label='Serie A',markerfacecolor='cyan', markersize=13),
                    Line2D([0], [0], marker='o', color='w', label='Serie B',markerfacecolor='yellow', markersize=13),
                    Line2D([0], [0], marker='o', color='w', label='Serie C',markerfacecolor='green', markersize=13),
                    Line2D([0], [0], marker='o', color='w', label='Serie D',markerfacecolor='red', markersize=13),
                    Line2D([0], [0], marker='o', color='w', label='Primavera',markerfacecolor='purple', markersize=13)]

pos = nx.kamada_kawai_layout(G)
nx.draw_networkx_nodes(G,pos,
                       nodelist=G.nodes,
                       node_size=size_map,
                       node_color=color_map,
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

ax.legend(handles=legend_elements1, loc='lower left', prop={'size': 8})
plt.axis('off')
plt.show()


#TOP 10 IN-DEGREE NODES
degrees_dict = {}

for t in degrees:
    degrees_dict[t[0]] = t[1]

degrees_list = sorted(degrees_dict.items(), key=lambda x: x[1], reverse=True)
top10_degree_nodes = degrees_list[:10]

print(top10_degree_nodes)

data = top10_degree_nodes

plt.bar(*zip(*data), color=sns.color_palette("ch:2,r=.2,l=.6"))

plt.title('Top 10 degree nodes')

plt.xlabel('Squadre')

plt.ylabel('Valori')

plt.xticks(rotation=15)

plt.show()





