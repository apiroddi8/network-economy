
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import networkx.algorithms.community as nxcom


df = pd.read_csv("Dataset/dataset_pulitoCUT07-21.csv")
df = df.dropna()


df = df.astype({'market_value': float },errors='raise')

df_filtered = df[(df['league_team1'] == 'ITA1') & (df['league_team2'] == 'ITA1')]
df_filtered = df_filtered[df_filtered['market_value'] >= 8000000.0]

#CREATE GRAPH
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


##COMMUNITY DETECTION WITH MODULARITY
communities = sorted(nxcom.greedy_modularity_communities(G), key=len, reverse=True)
#Count the communities
print(f"The Serie A has {len(communities)} communities.")


edges = [(v, w) for v, w, z in G.edges]


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


#Node size
size_map = []
in_degrees = G.in_degree
print('\n\n IN degree:',in_degrees)
for i in G.nodes:
    for node in in_degrees:
        if node[0] == i:
            in_degree = node[1]
    size_map.append(in_degree * 40)

# Set node and edge communities
set_node_community(G, communities)
set_edge_community(G)
node_color = [get_color(G.nodes[v]['community']) for v in G.nodes]
# Set community color for edges between members of the same community (internal) and intra-community edges (external)
external = [(v, w) for v, w, e in G.edges if G.edges[v, w, e]['community'] == 0]
internal = [(v, w) for v, w, e in G.edges if G.edges[v, w, e]['community'] > 0]
internal_color = ['black' for e in internal]

pos = nx.kamada_kawai_layout(G)
fig, ax = plt.subplots(figsize=(45, 35))
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

plt.axis('off')
plt.show()
