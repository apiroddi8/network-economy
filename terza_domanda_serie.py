import random
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


df=pd.read_csv('Dataset/dataset_completo10-15.csv')
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


dict_of_edges = (data3.groupby('player_name').apply(lambda x: list(map(tuple, zip(x['league_team1'],x['league_team2'])))).to_dict())
print('AAAAAA', dict_of_edges.items())


#

G = nx.MultiDiGraph()

for k,v in dict_of_edges.items():
    G.add_edges_from((edge for edge in v), player_ID = k)
#
# print("Edges with attributes: ",G.edges.data())
# print('Edges:', G.edges)
edgelist = G.edges
dict_edges_occurences = {}

for edge in edgelist:
    if (edge[0], edge[1]) not in dict_edges_occurences:
        dict_edges_occurences[(edge[0], edge[1])] = 1
    else:
        dict_edges_occurences[(edge[0], edge[1])] += 1

print(dict_edges_occurences)

color_map = []
for k,v in dict_edges_occurences.items():
        if k == ('ITA4', 'ITA1'):
            color_map.append('blue')
        elif k == ('ITA4', 'ITA2'):
            color_map.append('blue')
        elif k == ('ITA4', 'ITA3'):
            color_map.append('blue')
        elif k == ('ITA4', 'ITA4'):
            color_map.append('blue')
        elif k == ('ITA4', 'ITAJ'):
            color_map.append('blue')
        elif k == ('ITA4', 'OTH'):
            color_map.append('blue')
        elif k == ('ITA3', 'ITA1'):
            color_map.append('fuchsia')
        elif k == ('ITA3', 'ITA2'):
            color_map.append('fuchsia')
        elif k == ('ITA3', 'ITA3'):
            color_map.append('fuchsia')
        elif k == ('ITA3', 'ITA4'):
            color_map.append('fuchsia')
        elif k == ('ITA3', 'ITAJ'):
            color_map.append('fuchsia')
        elif k == ('ITA3', 'OTH'):
            color_map.append('fuchsia')
        elif k == ('ITA2', 'ITA1'):
            color_map.append('green')
        elif k == ('ITA2', 'ITA2'):
            color_map.append('green')
        elif k == ('ITA2', 'ITA3'):
            color_map.append('green')
        elif k == ('ITA2', 'ITA4'):
            color_map.append('green')
        elif k == ('ITA2', 'ITAJ'):
            color_map.append('green')
        elif k == ('ITA2', 'OTH'):
            color_map.append('green')
        elif k == ('ITA1', 'ITA1'):
            color_map.append('cyan')
        elif k == ('ITA1', 'ITA2'):
            color_map.append('cyan')
        elif k == ('ITA1', 'ITA3'):
            color_map.append('cyan')
        elif k == ('ITA1', 'ITA4'):
            color_map.append('cyan')
        elif k == ('ITA1', 'ITAJ'):
            color_map.append('cyan')
        elif k == ('ITA1', 'OTH'):
            color_map.append('cyan')
        elif k == ('ITAJ', 'ITA1'):
            color_map.append('orange')
        elif k == ('ITAJ', 'ITA2'):
            color_map.append('orange')
        elif k == ('ITAJ', 'ITA3'):
            color_map.append('orange')
        elif k == ('ITAJ', 'ITA4'):
            color_map.append('orange')
        elif k == ('ITAJ', 'ITAJ'):
            color_map.append('orange')
        elif k == ('ITAJ', 'OTH'):
            color_map.append('orange')
        else:
            color_map.append('black')


size_map = []
in_degrees = G.in_degree
for i in G.nodes:
    for node in in_degrees:
        if node[0] == i:
            in_degree = node[1]
    size_map.append(in_degree * 40)

for u,v,d in G.edges(data=True):
    d['weight'] = random.random()

edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())

labeldict = {}
labeldict["ITA1"] = "Serie A"
labeldict["ITA2"] = "Serie B"
labeldict["ITA3"] = "Serie C"
labeldict["ITA4"] = "Serie D"
labeldict["ITAJ"] = "Primavera"
labeldict["OTH"] = "Estere"

#Visualize the graph
fig, ax = plt.subplots(figsize=(45, 35))
fig.suptitle("Path player transfers from Serie D to Serie A")
pos = nx.spring_layout(G, k=0.3*1/np.sqrt(len(G.nodes())), iterations=20)

nx.draw_networkx_nodes(G, pos=pos, node_color = 'lightblue', node_size =size_map, alpha = 1 )

nx.draw_networkx_edges(G,
                       pos=pos,
                       edgelist = dict_edges_occurences.keys(),
                       width=list(i / 8 for i in dict_edges_occurences.values()),
                       edge_color=color_map,
                       alpha=0.6,
                       arrows= True,
                       arrowsize=15)

nx.draw_networkx_labels(G, pos=pos, font_size=7, labels=labeldict)

legend_elements1 = [Line2D([0], [0], marker='o', color='w', label='Serie A',markerfacecolor='cyan', markersize=13),
                    Line2D([0], [0], marker='o', color='w', label='Serie B',markerfacecolor='green', markersize=13),
                    Line2D([0], [0], marker='o', color='w', label='Serie C',markerfacecolor='fuchsia', markersize=13),
                    Line2D([0], [0], marker='o', color='w', label='Serie D',markerfacecolor='blue', markersize=13),
                    Line2D([0], [0], marker='o', color='w', label='Primavera',markerfacecolor='orange', markersize=13),
                    Line2D([0], [0], marker='o', color='w', label='Estere',markerfacecolor='black', markersize=13)]

ax.legend(handles=legend_elements1, loc='lower left', prop={'size': 8})
plt.axis('off')
plt.show()


##Compute trasfers numbers: method 1#######
distances = {key:len(value) for (key,value) in dict_of_edges.items()}
print(distances)
tot_trasferimenti = 0
tot_players = len(distances.keys())
for i in distances.values():
    tot_trasferimenti += i

mean_path_players = tot_trasferimenti / tot_players
print('Numero di trasferimenti medio per giocatore METODO 1: ', mean_path_players)

###Compute trasfers numbers: method 2#######
tot_trasferimenti2 = 0
for i in dict_edges_occurences.values():
    tot_trasferimenti2 += i

mean_path_players2 = tot_trasferimenti2 / tot_players
print('Numero di trasferimenti medio per giocatore METODO 2: ',mean_path_players2)



