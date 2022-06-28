import networkx as nx
import matplotlib.pyplot as plt
import random

# G = nx.Graph() #per creare un grafo non orientato. Se serve orientato g=DiGraph()
#
# G.add_node(0)  #qui aggiunge un solo nodo
# G.add_nodes_from( [1, 2, 3])
#
# G.add_edge(0,1)  #così aggiunge un lato tra 0 e 1
# G.add_edges_from([ (1,2), (2,3), (3,1) ])
#
# print("Number of nodes:", G.number_of_nodes())
# print("Number of edges:", G.number_of_edges())
#
# #Views
# print("G.nodes =", G.nodes)
# print("G.edges =", G.edges)
# print("G.degree =", G.degree)   #praticamente in ogni tupla il primo elemento rappresenta il nodo e il secondo il grado di quel nodo
# print("G.adj =", G.adj)         #è un dizionario a tre livelli, la prima chiave è il nodo il cui valore è un nuovo dizionario la cui
#                                 #chiave è il vicino del primo nodo e il valore è rappresentato dagli attributi della relazione tra i
#                                 #due nodi
#
#
# #Add attributes to nodes
# for i in G.nodes: # #1 most widely used graph operation
#     G.nodes[i]['smoking'] = False
#     G.nodes[i]['weight'] = random.choice(range(100,200))
# G.nodes[1]['smoking'] = True
# print("G.nodes.data():", G.nodes.data())  #questo restituisce una lista di tuple in cui il primo elemento è il nodo e il secondo
#                                           #elemento è un dizionario degli attributi del nodo
#
# #Add attributes to edges
# for e in G.edges: #also widely used operation
#     G.edges[e]['strength'] = round(random.random(), 2)
# print("G.edges.data():", G.edges.data())  #anche qui viene restituita una lista di tuple in cui viene mostrato l'attributo e il suo
#                                           #valore (nel dizionario) relativamente alla coppia di nodi indicata prima
# print("G.adj:", G.adj)
#
#
# #3 ways of iterating over the neighbors of a node
# # #2 most widely used operation in graphs
# print("Using G.adj[2]:")
# for nbr in G.adj[2]:
#     print(nbr)
#
# print("Using G[2]:")
# for nbr in G[2]:
#     print(nbr)
#
# print("Using G.neighbors(2):")
# for nbr in G.neighbors(2):    #questo è preferibile perchè è più comprensibile a livello di leggibilità, si capisce subito che si
#                             #sta iterando nei vicini del nodo 2
#     print(nbr)
#
# #Visualize the graph
# plt.figure(1)
# #Simple 1-line code: nx.draw_networkx(G)
# color_map = []
# size_map = []
# for i in G.nodes:
#     size_map.append(G.nodes[i]['weight']*2)
#     if G.nodes[i]['smoking']:
#         color_map.append('red')
#     else:
#         color_map.append('green')
# nx.draw_networkx( G,
#         node_color=color_map,
#         node_size=size_map,
#         pos=nx.spring_layout(G, iterations=1000),
#         arrows=False, with_labels=True )
# plt.show()
#
#
# #crea un grafico sulla distribuzione del grado Erdos dei nodi (fa un istogramma)
# plt.figure(2)
# G_Erdos = nx.erdos_renyi_graph(1000, 0.1)
# degrees = [G_Erdos.degree[i] for i in G_Erdos.nodes]   #qui sto creando una lista del grado dei nodi
# plt.xlabel('k')   #k sta per degree
# plt.ylabel('p_k')   #proprorzione di nodi che hanno quello specifico grado
# plt.title('Degree Distribution (Erdos-Renyi)')
# plt.hist(degrees, bins = range( min(degrees), max(degrees) ) )
#
# #Barabasi-Albert preferential attachment graph & degree distribution
# plt.figure(3)
# G_Barabasi = nx.barabasi_albert_graph(1000, 3)
# degrees = [G_Barabasi.degree[i] for i in G_Barabasi.nodes]
# plt.xlabel('k')
# plt.ylabel('p_k')
# plt.title('Degree Distribution (Barabasi-Albert)')
# plt.hist(degrees, bins = range( min(degrees), max(degrees) ) )
#
# plt.show()
#



################################### SIMULAZIONE GRAFO SECONDA DOMANDA #############################################################
dict_of_nodes = {'Player_1': [('C','A')], 'Player_2': [('C','B'), ('B','A') ]}
#print([val for sublist in dict_of_nodes.values() for val in sublist])
G = nx.Graph()

G.add_nodes_from( ['A', 'B', 'C'])
G.add_edges_from([val for sublist in dict_of_nodes.values() for val in sublist])


#Add attributes to edges
for e in G.edges:
    new_dict = {key:e for (key, values) in dict_of_nodes.items() if e in values}
    print(new_dict.keys())
    G.edges[e]['player_ID'] = new_dict.keys()


#print("G.edges.data():", G.edges.data())

# nx.add_path(G, ('B','A1'), id=100)
# nx.add_path(G, ('B','A2','A1'), id=101)
# nx.add_path(G, ('B', 'A3', 'A2', 'A1'), id=102)
# nx.add_path(G, ('B','A3', 'B', 'A1'), id=104)
#
# print("G.nodes =", G.nodes)
# print("G.edges =", G.edges)
#
# nx.draw(G)
# plt.show()







