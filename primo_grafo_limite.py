# 1)Tenendo conto di una soglia minima di valore del giocatore al momento del
# trasferimento, quali sono le squadre che nel campionato italiano
# più vengono coinvolte nella circolazione in entrata dei calciatori?

# Esiste una tendenza da parte della cerchia ristretta di top club a depredare
# le squadre di fasce più basse all’interno del medesimo campionato,
# è possibile individuare un accentramento di tutti gli acquisti rilevanti
# verso queste squadre? Quante sono? [confronto con altri paesi]

# NODI = squadre
# ARCHI = valore trasferimento esclusa soglia minima

# MEGLIO UTILIZZARE IL MARKET VALUE CHE E' PIù OGGETTIVO, MENTRE IL TRANSFER_VALUE E' PIù SOGGETTO A VARIAZIONI NEL CORSO DEL TEMPO
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
from networkx.algorithms.community import girvan_newman
import networkx.algorithms.community as nxcom

df = pd.read_csv("Dataset/dataset_pronto07-21.csv")
df = df.dropna()
df_serie = pd.read_csv("Dataset/STEP4.csv")

#print(df_serie.groupby(['league_team1']).sum())

# df = df.drop((df[df.team1  == 'AC Delta Porto Tolle']) | (df[df.team2  == 'AC Delta Porto Tolle']))
# df = df.drop((df[df.team1  == 'Terracina Calcio']) | (df[df.team2  == 'Terracina Calcio']))
# df = df.drop((df[df.team1  == 'ASD Comprensorio Casalnuovese']) | (df[df.team2  == 'ASD Comprensorio Casalnuovese']))
# df = df.drop((df[df.team1  == 'Imolese Calcio 1919']) | (df[df.team2  == 'Imolese Calcio 1919']))
# df = df.drop((df[df.team1  == 'SS Monopoli 1966']) | (df[df.team2  == 'SS Monopoli 1966']))
# df = df.drop((df[df.team1  == 'Riviera Marmi']) | (df[df.team2  == 'Riviera Marmi']))


print(df['market_value'])
df = df.astype({'market_value': float },errors='raise')

df_filtered = df[(df['country_team1'] == 'Italy') & (df['country_team2'] == 'Italy')]
df_filtered = df_filtered[df_filtered['market_value'] >= 15000000.0 ]    #8000000.0 per fare grafo con poche squadre e milan juve centrali
print(df_filtered)
#
G=nx.from_pandas_edgelist(df_filtered, "team1", "team2",create_using=nx.MultiDiGraph)
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

print("G.nodes =", G.nodes)
#print("\n\nG.edges =", G.edges)
# print("\n\n\nG.degree =", G.degree)

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
#

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
fig.suptitle("football player transfer from 2009 to 2021")
#Simple 1-line code: nx.draw_networkx(G)
color_map = []
size_map = []
in_degrees = G.in_degree
for i in G.nodes:
    for node in in_degrees:
        if node[0] == i:
            in_degree = node[1]
    size_map.append(in_degree * 20)


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
                        font_size=5)  # 7 per lo zoom

plt.show()

#nx.write_gml(G, '../../Desktop/graph_1A.gml')








