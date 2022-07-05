import pandas as pd
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

# top=['ITA1','SPA1','ENG1','GER1','FRA1','POR1','NED1']
# #
# pulito=pd.read_csv('df_7_file.csv')
# # pulito=pulito[(pulito['league_team1']=='ITA1')|(pulito['league_team1']=='ENG1')|(pulito['league_team1']=='FRA1')|(pulito['league_team1']=='POR1')
# #                 |(pulito['league_team1']=='SPA1')|(pulito['league_team1']=='GER1')|(pulito['league_team1']=='NED1')|(pulito['league_team2']=='ENG1')
# #                 |(pulito['league_team2']=='ITA1')|(pulito['league_team2']=='FRA1')|(pulito['league_team2']=='NED1')|(pulito['league_team2']=='POR1')
# #                 |(pulito['league_team2']=='GER1')|(pulito['league_team2']=='SPA1')]
# #
# pulito_market=pulito.Costo
# #
# pulito_market.to_csv('ora.csv',index=False)
#
# # df7=pd.read_csv('df_7_file.csv')
# # df7_transfer=df7.MarketValue
# # df7_transfer.to_csv('df_7_market')
#
# # dataset_finale=pd.read_csv('pulito15_18.csv')
# # #dataset_finale.drop(columns=['fee','dealing_country'],inplace=True,axis=1)
# # dataset_finale=dataset_finale.market_value
# # dataset_finale.to_csv('pulito15_18market.csv')

finale=pd.read_csv('dataset_finale.csv')
#finale10=finale[finale['season']==2010]
finale12_13=finale[(finale['season']==2011)|(finale['season']==2012)|(finale['season']==2013)|(finale['season']==2014)|(finale['season']==2015)]
finale12_13.to_csv('dataset_finale11-15.csv')


#
# del finale10_11['Unnamed: 0']
# del finale12_13['Unnamed: 0']
#
# finale10_11.to_csv('dataset_finale10_11',index=False)
# finale12_13.to_csv('dataset_finale12_13',index=False)

# df7=pd.read_csv('df_7_file.csv')
# df7tagliato=df7[['Club','Costo','Movement']]
# df7tagliato['Costo']=df7tagliato['Costo'].fillna('-')
# df7tagliato.to_csv('df_7_fileTAGLIATO.csv')
