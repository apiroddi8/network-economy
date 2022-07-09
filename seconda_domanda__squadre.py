import random
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


df=pd.read_csv('Dataset/dataset_completo10-15.csv')
df_serie = pd.read_csv('Dataset/STEP4.csv')

new_df=df.groupby('player_name').first().reset_index()
print(new_df)
new_df2=new_df[new_df['league_team1']=='ITA4']
print(new_df2)
player_list=new_df2['player_name'].tolist()
dataframe=df[df['player_name'].isin(player_list)]
print(dataframe)
new_dataframe=dataframe[dataframe['league_team2']=='ITA1']
player_list2=list(set(new_dataframe['player_name'].tolist()))
print(player_list2)

data=dataframe[dataframe['player_name'].isin(player_list2)]
esclusi=[]
salvati=[]
print(data)
print(len(data.index))
righe=list(range(0,len((data.index))))
print(righe)
data['indice']=righe
print(data)
print(player_list)
for player in player_list2:
    for row in data.itertuples():
        if row.player_name==player:
            for row2 in data.itertuples():
                if ((row2.season == row.season or row2.season==row.season+1) and row2.league_team2!='ITA1' and row2.player_name==player and row2.indice!=row.indice):
                    for row3 in data.itertuples():
                        if (row3.indice!=row2.indice and row3.indice!=row.indice and row3.league_team2=='ITA1' and row3.player_name==player):
                            #esclusi.append(player)
                            salvati.append(player)
                    if player not in salvati:
                        esclusi.append(player)


data2=data[~data['player_name'].isin(esclusi)]
data2.sort_values(['player_name','indice'], ascending=[True, True], inplace=True)

###### QUIIIII

bandiere=[]

segnale=['ok']
for raw in data2.itertuples():
    check=True
    if raw.league_team2=='ITA1' and raw.player_name!=segnale[-1]:
        for raw2 in data2.itertuples():
            if (raw2.indice > raw.indice and (raw2.season==raw.season or raw2.season==raw.season+1) and raw2.league_team2!='ITA1' and raw2.player_name==raw.player_name):
                bandiere.append('red')
                check=False
                break
        if check:
            bandiere.append('green')
            segnale.append(raw.player_name)

    else:
        bandiere.append('red')

print(len(bandiere))
data2['bandiere']=bandiere

print(data2)

data2 = data2.astype({'indice': int },errors='raise')

player_list3 = data2.player_name.unique().tolist()
indice = {}
for player in player_list3:
    for row in data2.itertuples():
            if row.bandiere == 'green' and row.player_name == player:
                if row.player_name not in indice.keys():
                    indice[player] = row.indice


print(indice)
#print(data2)
for index, row in data2.iterrows():
    for player, ind in indice.items():
        if row.indice < ind and row.player_name == player:
            data2.at[index,'bandiere'] = 'green'

data3 = data2[data2['bandiere'] == 'green']

data3.loc[(data2['league_team1']!='ITA1')& (data2['league_team1']!='ITA2')&
          (data2['league_team1']!='ITA3')& (data2['league_team1']!='ITA4')&
          (data2['league_team1']!='ITAJ'),'league_team1']='OTH'

data3.loc[(data2['league_team2']!='ITA1')& (data2['league_team2']!='ITA2')&
          (data2['league_team2']!='ITA3')& (data2['league_team2']!='ITA4')&
          (data2['league_team2']!='ITAJ'),'league_team2']='OTH'


#print('dopo modifica bandiera\n',data2)
data3.loc[(data2['league_team1']!='ITA1')& (data2['league_team1']!='ITA2')&
          (data2['league_team1']!='ITA3')& (data2['league_team1']!='ITA4')&
          (data2['league_team1']!='ITAJ'),'team1']='Estera'

data3.loc[(data2['league_team2']!='ITA1')& (data2['league_team2']!='ITA2')&
          (data2['league_team2']!='ITA3')& (data2['league_team2']!='ITA4')&
          (data2['league_team2']!='ITAJ'),'team2']='Estera'


dict_of_edges = (data3.groupby('player_name').apply(lambda x: list(map(tuple, zip(x['team1'],x['team2'])))).to_dict())
print('AAAAAA', dict_of_edges.items())


G = nx.MultiDiGraph()

for k,v in dict_of_edges.items():
    G.add_edges_from((edge for edge in v), player_ID = k)

print("Edges with attributes: ",G.edges.data())

team_list = df_serie.team1.to_list()

for node in G.nodes:
    if node in team_list:
        G.nodes[node]['league_team'] = prova = df_serie.loc[(df_serie['team1'] == node), 'league_team1'].to_list()[0]
    else:
        G.nodes[node]['league_team'] = 'other'

in_degrees = G.in_degree
out_degrees = G.out_degree
# # Identify nodes for removal
nodes2remove_indegrees = [node[0] for node in in_degrees if node[1] < 2 ]
nodes2remove_outdegrees = [node[0] for node in out_degrees if node[1] <= 1 ]
nodes2remove1 = set(nodes2remove_indegrees)
nodes2remove2 = set(nodes2remove_outdegrees)
nodes2remove3 = list(nodes2remove1.intersection(nodes2remove2))

# # Remove target-nodes
for node in nodes2remove3:
    G.remove_node(node)
#
# for k,v in G.nodes(data=True):
#     print(k,v['league_team'])

edgelist = G.edges
dict_edges_occurences = {}

for edge in edgelist:
    if (edge[0], edge[1]) not in dict_edges_occurences:
        dict_edges_occurences[(edge[0], edge[1])] = 1
    dict_edges_occurences[(edge[0], edge[1])] += 1

print(dict_edges_occurences)

print(G.nodes(data=True))
serieD = [nodo for nodo, at in G.nodes(data=True) if at['league_team'] == 'ITA4']
serieA = [nodo for nodo, at in G.nodes(data=True) if at['league_team'] == 'ITA1']

bw_centrality = nx.betweenness_centrality_subset(G, sources= serieD, targets= serieA, normalized=False)

print("\n\nBetweenness Centrality: ", bw_centrality)


size_map = []
for i in G.nodes:
    for node, bw in bw_centrality.items():
        if node == i:
            size_map.append((bw + 1 ) * 50)


for u,v,d in G.edges(data=True):
    d['weight'] = random.random()

edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())
#
## pos = nx.kamada_kawai_layout(G)
pos = nx.spring_layout(G, k=0.9*1/np.sqrt(len(G.nodes())), iterations=20)

nx.draw_networkx_nodes(G, pos=pos, node_color = 'lightblue', node_size =size_map, alpha = 1 )

nx.draw_networkx_edges(G,
                       pos=pos,
                       edgelist = dict_edges_occurences.keys(),
                       width=list(i / 10 for i in dict_edges_occurences.values()),
                       edge_color='green',
                       alpha=0.6,
                       arrows= True,
                       arrowsize=15)

nx.draw_networkx_labels(G, pos=pos, font_size=7)

plt.axis('off')
plt.show()


# # nx.draw_networkx_edges(G, pos=pos, edgelist=edges,
# #                      edge_color=weights, width=list(i / 20 for i in dict_edges_occurences.values()), edge_cmap=plt.cm.Blues)

#calcolare betweennes soltanto dei percorsi minimali tra i nodi ITA4 ed Ita1
#quindi aggiungi label al nodo della league_team