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
import itertools

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
from networkx.algorithms.community import girvan_newman
import networkx.algorithms.community as nxcom


df = pd.read_csv("Dataset/dataset_finale11-15pronto.csv")
df = df.dropna()
df_serie = pd.read_csv("Dataset/STEP4.csv")

#print(df_serie.groupby(['league_team1']).sum())

# df = df.drop((df[df.team1  == 'AC Delta Porto Tolle']) | (df[df.team2  == 'AC Delta Porto Tolle']))
# df = df.drop((df[df.team1  == 'Terracina Calcio']) | (df[df.team2  == 'Terracina Calcio']))
# df = df.drop((df[df.team1  == 'ASD Comprensorio Casalnuovese']) | (df[df.team2  == 'ASD Comprensorio Casalnuovese']))
# df = df.drop((df[df.team1  == 'Imolese Calcio 1919']) | (df[df.team2  == 'Imolese Calcio 1919']))
# df = df.drop((df[df.team1  == 'SS Monopoli 1966']) | (df[df.team2  == 'SS Monopoli 1966']))
# df = df.drop((df[df.team1  == 'Riviera Marmi']) | (df[df.team2  == 'Riviera Marmi']))


#print(df['market_value'])
df = df.astype({'market_value': float },errors='raise')
first_quartile_market_value = df['market_value'].quantile(q=0.75)
#print(first_quartile_market_value)

#df_filtered = df[(df['country_team1'] == 'England') & (df['country_team2'] == 'England')]
df_filtered = df[(df['league_team1'] == 'ITA1') & (df['league_team2'] == 'ITA1')]
#df_filtered=df
df_filtered = df_filtered[df_filtered['market_value'] >= first_quartile_market_value]
#print(df_filtered)
#
G=nx.from_pandas_edgelist(df_filtered, "team1", "team2",create_using=nx.MultiDiGraph)
#print("Number of nodes:", G.number_of_nodes())
#print("Number of edges:", G.number_of_edges())

# print("G.nodes =", G.nodes)
print("\n\nG.edges =", G.edges)
# print("\n\n\nG.degree =", G.degree)


#COUNTING NUMBER OF EDGES BETWEEN ANY TWO NODES
edgelist = G.edges
dict_edges_occurences = {}

for edge in edgelist:
    if (edge[0], edge[1]) not in dict_edges_occurences:
        dict_edges_occurences[(edge[0], edge[1])] = 1
    dict_edges_occurences[(edge[0], edge[1])] += 1



#PUNTO B
#devo riuscire a colorare i nodi in base al cluster di appartenenza. I clusters vengono definiti in base alle squadre che tra di loro effettuano la maggior parte dei trasferimenti
# GUIDA MOLTO CARINA https://networkx.guide/algorithms/community-detection/girvan-newman/

#communities based on Girvan-Newman edge betwenness centrality algorithm --> calcola la edge betwenness e poi toglie l'edge con la betwennesss centrality più alta, ricalcola la edge betwenness
#                                                                            per i restanti edge e toglie quello con la betwenness più alto e va avanti così finche non rimangono più edges.
#### SPOILER: NON FUNZIONA NEL NOSTRO GRAFO
# k = 4
# comp = girvan_newman(G)
# for communities in itertools.islice(comp, k):
#     print(tuple(sorted(c) for c in communities))
#
import itertools
k = 17
comp = girvan_newman(G)
for communities in itertools.islice(comp, k):
    print(tuple(sorted(c) for c in communities))

communities = next(comp)
print(len(communities))

def set_node_community(G, communities):
    '''Add community to node attributes'''
    for c, v_c in enumerate(communities):
        for v in v_c:
            # Add 1 to save 0 for external edges
            G.nodes[v]['community'] = c + 1

def set_edge_community(G):
    '''Find internal edges and add their community to their attributes'''
    for v, w, e in G.edges:
        if G.nodes[v]['community'] == G.nodes[w]['community']:
            # Internal edge, mark with community
            G.edges[v, w, e]['community'] = G.nodes[v]['community']
        else:
            # External edge, mark as 0
            G.edges[v, w, e]['community'] = 0

def get_color(i, r_off=1, g_off=1, b_off=1):
    '''Assign a color to a vertex.'''
    r0, g0, b0 = 0, 0, 0
    n = 16
    low, high = 0.1, 0.9
    span = high - low
    r = low + span * (((i + r_off) * 3) % n) / (n - 1)
    g = low + span * (((i + g_off) * 5) % n) / (n - 1)
    b = low + span * (((i + b_off) * 7) % n) / (n - 1)
    return (r, g, b)


plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams.update({'figure.figsize': (15, 10)})
plt.suptitle("Communities with Girvan Newman")
# Set node and edge communities
set_node_community(G, communities)
set_edge_community(G)
# Set community color for nodes
node_color = [get_color(G.nodes[v]['community']) for v in G.nodes]
# Set community color for internal edges
external = [(v, w) for v, w, e in G.edges if G.edges[v, w, e]['community'] == 0]
internal = [(v, w) for v, w, e in G.edges if G.edges[v, w, e]['community'] > 0]
internal_color = ['gray' for e in internal]
pos = nx.kamada_kawai_layout(G)
#Node size
size_map = []
in_degrees = G.in_degree
print('\n\n IN degree:',in_degrees)
for i in G.nodes:
    for node in in_degrees:
        if node[0] == i:
            in_degree = node[1]
    size_map.append(in_degree * 40)
#Draw external edges
nx.draw_networkx(
    G, pos=pos, node_size=0,
    edgelist=external, edge_color="#333333", with_labels=False)
# Draw nodes and internal edges
nx.draw_networkx(
    G, pos=pos, node_size=size_map, node_color=node_color,
    edgelist=internal, edge_color=internal_color)


plt.show()

nx.write_gml(G, 'test_graph.gml')



## alternativa 2
communities = sorted(nxcom.greedy_modularity_communities(G), key=len, reverse=True)
    # Count the communities
print(f"The karate club has {len(communities)} communities.")

print('NODI')
edges = [(v, w) for v, w, z in G.edges]

print(edges)


def set_node_community(G, communities):
    '''Add community to node attributes'''
    for c, v_c in enumerate(communities):
        for v in v_c:
            # Add 1 to save 0 for external edges
            G.nodes[v]['community'] = c + 1

def set_edge_community(G):
    '''Find internal edges and add their community to their attributes'''
    for v, w, e in G.edges:
        if G.nodes[v]['community'] == G.nodes[w]['community']:
            # Internal edge, mark with community
            G.edges[v, w, e]['community'] = G.nodes[v]['community']
        else:
            # External edge, mark as 0
            G.edges[v, w, e]['community'] = 0

def get_color(i, r_off=1, g_off=1, b_off=1):
    '''Assign a color to a vertex.'''
    r0, g0, b0 = 0, 0, 0
    n = 16
    low, high = 0.1, 0.9
    span = high - low
    r = low + span * (((i + r_off) * 3) % n) / (n - 1)
    g = low + span * (((i + g_off) * 5) % n) / (n - 1)
    b = low + span * (((i + b_off) * 7) % n) / (n - 1)
    return (r, g, b)


# Set node and edge communities
set_node_community(G, communities)
set_edge_community(G)
node_color = [get_color(G.nodes[v]['community']) for v in G.nodes]
# Set community color for edges between members of the same community (internal) and intra-community edges (external)
external = [(v, w) for v, w, e in G.edges if G.edges[v, w, e]['community'] == 0]
internal = [(v, w) for v, w, e in G.edges if G.edges[v, w, e]['community'] > 0]
internal_color = ['black' for e in internal]

pos = nx.kamada_kawai_layout(G)
plt.rcParams.update({'figure.figsize': (15, 10)})
plt.suptitle("Communities with Modularity")
# Draw external edges
nx.draw_networkx(
    G,
    pos=pos,
    node_size=0,
    edgelist=external,
    edge_color="silver")
# Draw nodes and internal edges
nx.draw_networkx(
    G,
    pos=pos,
    node_color=node_color,
    node_size=size_map,
    edgelist=internal,
    edge_color=internal_color)

plt.show()
