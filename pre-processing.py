import pandas as pd
from collections import defaultdict
#
#CARICAMENTO DATASET:
df_nostro= pd.read_csv('dataset_grezzo10.csv')
df_agg1=pd.read_csv('dataset//dataset_aggiuntivo1.csv.csv')
df_agg2=pd.read_csv('dataset/dataset_aggiuntivo2.csv')


#
#RINOMINAZIONE COLONNE:
df_nostro.rename(columns = {'league':'league_team1', 'team_name':'team1', 'team_country':'country_team1',
                     'counter_team_name':'team2','counter_team_country':'country_team2',
                     'transfer_fee_amnt':'transfer_value','market_val_amnt':'market_value'}, inplace = True)

#print(df_nostro.to_string())
print(len(df_nostro.index))

print('##########################################')

#RINOMINAZIONE VALORI COLONNA LEGHE:
df_nostro['league_team1'].replace('IT1','ITA1',inplace=True)
df_nostro['league_team1'].replace('IT2','ITA2',inplace=True)
df_nostro['league_team1'].replace(['ITJ1','ITJ2','IJ1','IJ2A','IJ2B'],'ITAJ',inplace=True)
df_nostro['league_team1'].replace(['IT3A','IT3B','IT3C'],'ITA3',inplace=True)
df_nostro['league_team1'].replace('ES1','SPA1',inplace=True)
df_nostro['league_team1'].replace('GB1','ENG1',inplace=True)
df_nostro['league_team1'].replace('L1','GER1',inplace=True)
df_nostro['league_team1'].replace('FR1','FRA1',inplace=True)
df_nostro['league_team1'].replace('PO1','POR1',inplace=True)
df_nostro['league_team1'].replace('NL1','NET1',inplace=True)


#print(df_nostro.to_string())
print(len(df_nostro.index))

print('################################################')

#CREAZIONE DELLA COLONNA CHE CONTIENE LA LEGA DI APPARTENENZA DEL TEAM 2
#IL DATASET INIZIALMENTE HA SOLTANTO LA COLONNA DELLA LEGA DI APPARTENENZA DEL TEAM 1:
lista_colonna_league2=[]

for row in df_nostro.itertuples():
    top_countries=['England','Spain','Germany','Portugal','France','Netherlands']
    if any([row.country_team2 == top_country for top_country in top_countries]):
        if row.team2 in set(list(df_nostro[(df_nostro['league_team1']==row.country_team2[:3].upper()+'1') & (df_nostro['season']==row.season)]['team1'])):
            lista_colonna_league2.append(row.country_team2[:3].upper()+'1')
        else:
            lista_colonna_league2.append(row.country_team2[:3].upper()+'2')

    elif row.country_team2=='Italy':

        if  len(list(df_nostro[(df_nostro['team1'] == row.team2)& (df_nostro['season'] == row.season)]['league_team1']))>0:
            lista_colonna_league2.append(list(df_nostro[(df_nostro['team1'] == row.team2)]['league_team1'])[0])######
        elif len(list(df_nostro[(df_nostro['team1']==row.team2)]['league_team1']))>0:
            lista_colonna_league2.append(list(df_nostro[(df_nostro['team1']==row.team2)& (df_nostro['season']==row.season)]['league_team1'])[0])########
        else:
            lista_colonna_league2.append(row.country_team2[:3].upper()+'4')
    else:
        lista_colonna_league2.append(row.country_team2[:3].upper())


print('########################')
#print(lista_colonna_league2)
print('#######################')

df_nostro['league_team2']=lista_colonna_league2

#print(df_nostro.to_string())
print(len(df_nostro.index))

print('###########################')




#ELIMINAZIONE TRANSFER ID DUPLICATI, RESTANO SOLO I LEFT:
df_nostro.drop_duplicates(subset='transfer_id',ignore_index=True,inplace=True)

#print(df_nostro.to_string())
print(len(df_nostro.index))

condition = df_nostro['dir'] == 'in'

df_nostro.loc[condition, ['team1', 'team2']] = (
    df_nostro.loc[condition, ['team2', 'team1']].values)

df_nostro.loc[condition, ['country_team1', 'country_team2']] = (
    df_nostro.loc[condition, ['country_team2', 'country_team1']].values)

df_nostro.loc[condition, ['league_team1', 'league_team2']] = (
    df_nostro.loc[condition, ['league_team2', 'league_team1']].values)

# print(df_nostro.team1)
# print(df_nostro.team2)
# print(df_nostro.country_team1)
# print(df_nostro.country_team2)

df_nostro['dir'].replace(['in'],'left',inplace=True)

#print(df_nostro.to_string())
print(len(df_nostro.index))

# df_nostro2=df_nostro.drop_duplicates(subset=['team1','season','window','player_name','team2'],ignore_index=True,inplace=False)
#
# #print(df_nostro.to_string())
# print(len(df_nostro2.index))
#
# print(df_nostro[~df_nostro.apply(tuple,1).isin(df_nostro2.apply(tuple,1))])




#CHECK, PER OGNI STAGIONE, CHE TUTTE LE SQUADRE DEL CAMPIONATO SIANO PRESENTI:
# print(len(set(list(df_nostro[(df_nostro['league_team1']=='PO1') & (df_nostro['season']==2021)]['team1']))))
# print(len(set(list(df_nostro[(df_nostro['league_team1']=='PO1') & (df_nostro['season']==2020)]['team1']))))
# print(len(set(list(df_nostro[(df_nostro['league_team1']=='PO1') & (df_nostro['season']==2019)]['team1']))))
# print(len(set(list(df_nostro[(df_nostro['league_team1']=='PO1') & (df_nostro['season']==2018)]['team1']))))
# print(len(set(list(df_nostro[(df_nostro['league_team1']=='PO1') & (df_nostro['season']==2017)]['team1']))))
# print(len(set(list(df_nostro[(df_nostro['league_team1']=='PO1') & (df_nostro['season']==2016)]['team1']))))
# print(len(set(list(df_nostro[(df_nostro['league_team1']=='PO1') & (df_nostro['season']==2015)]['team1']))))
# print(len(set(list(df_nostro[(df_nostro['league_team1']=='PO1') & (df_nostro['season']==2014)]['team1']))))
# print(len(set(list(df_nostro[(df_nostro['league_team1']=='PO1') & (df_nostro['season']==2013)]['team1']))))
# print(len(set(list(df_nostro[(df_nostro['league_team1']=='PO1') & (df_nostro['season']==2012)]['team1']))))
# print(len(set(list(df_nostro[(df_nostro['league_team1']=='PO1') & (df_nostro['season']==2011)]['team1']))))
# print(len(set(list(df_nostro[(df_nostro['league_team1']=='PO1') & (df_nostro['season']==2010)]['team1']))))
# print(len(set(list(df_nostro[(df_nostro['league_team1']=='PO1') & (df_nostro['season']==2009)]['team1']))))


#CONTEGGIO NA DELLE VARIE COLONNE PRIMA DELLA PULIZIA:
print('CONTEGGIO NA PRE PULIZIA\n')

for column in df_nostro.columns:
    print(column,df_nostro[f'{column}'].isna().sum())

#ELIMINAZIONE COLONNE INUTILI:
df_nostro.drop(columns=['player_nation2','team_id','counter_team_id'],inplace=True,axis=1)
#print(df_nostro.to_string())

#ELIMINAZIONE DEGLI NA CHE RAPPRESENTANO UNA PARTE NON SIGNIFICATIVA DEL TOTALE DELLE OSSERVAZIONI:
df_nostro.dropna(subset=['player_age','player_nation','country_team2','transfer_id'],inplace=True)
#print(df_nostro.to_string())

#OTTENIMENTO DELLA LISTA DI TUTTI I RUOLI DI TRANSFERMARKT (PRESI UNA SOLA VOLTA):
print(df_nostro.player_pos.unique())



#ACCORPAMENTO DEI VARI RUOLI NELLE 4 MACROCATEGORIE: PORTIERE, DIFENSORE, CENTROCAMPISTA, ATTACCANTE:
df_nostro['player_pos'].replace(['GK'],'goalkeeper',inplace=True)
df_nostro['player_pos'].replace(['RB','CB','LB','defence'],'defender',inplace=True)
df_nostro['player_pos'].replace(['CM','AM','DM','LM','RM','midfield'],'midfielder',inplace=True)
df_nostro['player_pos'].replace(['CF','SS','LW','RW','attack'],'striker',inplace=True)
#df_nostro['age_cat'] = pd.cut(df['age'], bins=[0,23,54,56, 999], labels=['Young', 'Adult', 'Elder','other'])
#print(df_nostro.to_string())

#ASSEGNAZIONE DEL VALORE ZERO AL VALORE DEL TRASFERIMENTO QUANDO IS FREE= TRUE; IS END LOAN= TRUE, TEAM2=WITHOUT CLUB:
df_nostro.loc[(df_nostro['is_loan_end'] == True) |(df_nostro['is_retired']==True)| (df_nostro['is_free']==True) | (df_nostro['team2']=='Without Club'), 'transfer_value'] = 0.0

#print(df_nostro.to_string())
#
# #CONTEGGIO DEGLI NA UNA VOLTA TERMINATA LA PULIZIA:
print('CONTEGGIO NA POST PULIZIA \n')

for column in df_nostro.columns:
    print(column,df_nostro[f'{column}'].isna().sum())
#
#
# #LA COLONNA DELL'ETA HA VALORI DI TIPO STRINGA, DOVREBBERO ESSERE INVECE NUEMERICI
# #CONVERTIAMO TUTTI I VALORI DELLA COLONNA ETA PRIMA IN FLOAT E POI IN INTERI:
df_nostro=df_nostro.astype({'player_age':float})
df_nostro=df_nostro.astype({'player_age':int})

#print(df_nostro.to_string())

#CONTEGGIO DEL TIPO DI VALORI ALL'INTERNO DI CIASCUNA COLONNA:
for column in df_nostro.columns:
    print(column)
    print('numero stringhe', sum([1 for row in df_nostro[f'{column}']if type(row)==str]))
    print('numero float', sum([1 for row in df_nostro[f'{column}'] if type(row) == float]))
    print('numero interi', sum([1 for row in df_nostro[f'{column}'] if type(row) == int]))
    print('numero booleani', sum([1 for row in df_nostro[f'{column}'] if type(row) == bool]))



#########################################################################################################
#########################################################################################################
#########################################################################################################


#OTTENIMENTO DEI VALORI MANCANTI DEL MARKET VALUE ANDANDOLI A PESCARE DAL DATASET DEI COLLEGHI CAGLIARITANI:
dict_na={}

dict_na['giocatori']=df_nostro['player_name'].tolist()
dict_na['squadre_partenza']=df_nostro['team1'].tolist()
dict_na['squadre_arrivo']=df_nostro['team2'].tolist()
dict_na['eta']=df_nostro['player_age'].tolist()
dict_na['finestre']=df_nostro['window'].tolist()


condition2 = df_agg2['movement'] == 'in'

df_agg2.loc[condition2, ['club', 'dealing_club']] = (
    df_agg2.loc[condition2, ['dealing_club', 'club']].values)

df_agg2['movement'].replace(['in'],'out',inplace=True)


df_agg2['market_value']=df_agg2['market_value'].fillna('-')



condition3 = df_agg1['Movement'] == 'In'

df_agg1.loc[condition3, ['Club', 'ClubInvolved']] = (
    df_agg1.loc[condition3, ['ClubInvolved', 'Club']].values)

df_agg1['Movement'].replace(['In'],'Out',inplace=True)

df_agg1['Costo'] = df_agg1['Costo'].fillna("-")
df_agg1['Costo']=df_agg1['Costo'].str.findall('(?<=:).*$').apply(','.join)
df_agg1['Costo'][df_agg1['Costo']=='']='0 €'




lista_market_values=[]


for segnalibro in range(0,len(dict_na['giocatori'])):
    check=False
    for row in df_agg2.itertuples():

        if (row.name==dict_na['giocatori'][segnalibro] and row.club==dict_na['squadre_partenza'][segnalibro] and
                 row.dealing_club== dict_na['squadre_arrivo'][segnalibro] and str(row.age)[:2]==str(dict_na['eta'][segnalibro])):

            #print('ok1')
            lista_market_values.append(row.market_value)
            check=True
            break

        elif (row.name==dict_na['giocatori'][segnalibro] and str(row.age)[:2]==str(dict_na['eta'][segnalibro])):
            #print('ok3')
            lista_market_values.append(row.market_value)
            check = True
            break

    if not check:
        lista_market_values.append('NF')

df_nostro['market_value']=lista_market_values

print(lista_market_values[:100])
print(len(lista_market_values))

print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

lista_market_values2=[]

dict_na2 = {}


dict_na2['giocatori'] = df_nostro.loc[(df_nostro['market_value'] == '-')|(df_nostro['market_value']=='NF'), 'player_name'].tolist()
dict_na2['squadre_partenza'] = df_nostro.loc[(df_nostro['market_value'] == '-')|(df_nostro['market_value']=='NF'), 'team1'].tolist()
dict_na2['squadre_arrivo'] = df_nostro.loc[(df_nostro['market_value'] == '-')|(df_nostro['market_value']=='NF'), 'team2'].tolist()
dict_na2['eta'] = df_nostro.loc[(df_nostro['market_value'] == '-')|(df_nostro['market_value']=='NF'), 'player_age'].tolist()

for segnalibro in range(0,len(dict_na2['giocatori'])):
    check=False
    for row in df_agg1.itertuples():

        if (row.Name==dict_na2['giocatori'][segnalibro] and row.Club==dict_na2['squadre_partenza'][segnalibro] and
                 row.ClubInvolved== dict_na2['squadre_arrivo'][segnalibro] and str(row.Età)==str(dict_na2['eta'][segnalibro])) :

            #print('ok2')
            lista_market_values2.append(row.MarketValue)
            check=True
            break

        elif (row.Name==dict_na2['giocatori'][segnalibro] and str(row.Età)==str(dict_na2['eta'][segnalibro])):
            #print('ok3')
            lista_market_values2.append(row.MarketValue)
            check = True
            break

    if not check:
        lista_market_values2.append('NF')
        #print(dict_na['giocatori'][segnalibro])

print(lista_market_values2[:100])
print(len(lista_market_values2))

print(len(df_nostro.index))


df_nostro.market_value[(df_nostro.market_value=='-')|df_nostro.market_value=='NF']=lista_market_values2
print(type(df_nostro.market_value[0]))

print(df_nostro.market_value)




print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')



#df_nostro.loc[pd.isnull(df['A']), 'A'] = mylist
#df_nostro.loc[pd.isnull(df_nostro['market_value']),'market_value']=lista_market_values


#OTTENIMENTO DEI VALORI MANCANTI DEL TRANSFER VALUE ANDANDOLI A PESCARE DAL DATASET DEI COLLEGHI CAGLIARITANI:

df_agg2['fee']=df_agg2['fee'].fillna('-')

dict_na3 = {}


dict_na3['giocatori'] = df_nostro.loc[df_nostro['transfer_value'].isnull(), 'player_name'].tolist()
dict_na3['squadre_partenza'] = df_nostro.loc[df_nostro['transfer_value'].isnull(), 'team1'].tolist()
dict_na3['squadre_arrivo'] = df_nostro.loc[df_nostro['transfer_value'].isnull(), 'team2'].tolist()
dict_na3['eta'] = df_nostro.loc[df_nostro['transfer_value'].isnull(), 'player_age'].tolist()





lista_transfer_values=[]


for segnalibro in range(0,len(dict_na3['giocatori'])):
    check=False
    for row in df_agg2.itertuples():

        if (row.name==dict_na3['giocatori'][segnalibro] and row.club==dict_na3['squadre_partenza'][segnalibro] and
                 row.dealing_club== dict_na3['squadre_arrivo'][segnalibro] and str(row.age)[:2]==str(dict_na3['eta'][segnalibro])):

            #print('ok1')
            lista_transfer_values.append(row.fee)
            check=True
            break

    if not check:
        lista_transfer_values.append('NF')
        #print(dict_na['giocatori'][segnalibro])





print(lista_transfer_values[:100])
print(len(lista_transfer_values))

print(len(df_nostro.index))

df_nostro.loc[pd.isnull(df_nostro['transfer_value']),'transfer_value']=lista_transfer_values
print(type(df_nostro.transfer_value[0]))
#df_nostro['transfer_value']=lista_transfer_values



print(df_nostro.transfer_value)

print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')



dict_na4 = {}



dict_na4['giocatori'] = df_nostro.loc[(df_nostro['transfer_value'] == '-')|(df_nostro['transfer_value']=='NF')|(df_nostro['transfer_value']=='?'), 'player_name'].tolist()
dict_na4['squadre_partenza'] = df_nostro.loc[(df_nostro['transfer_value'] == '-')|(df_nostro['transfer_value']=='NF')|(df_nostro['transfer_value']=='?'), 'team1'].tolist()
dict_na4['squadre_arrivo'] = df_nostro.loc[(df_nostro['transfer_value'] == '-')|(df_nostro['transfer_value']=='NF')|(df_nostro['transfer_value']=='?'), 'team2'].tolist()
dict_na4['eta'] = df_nostro.loc[(df_nostro['transfer_value'] == '-')|(df_nostro['transfer_value']=='NF')|(df_nostro['transfer_value']=='?'), 'player_age'].tolist()
lista_transfer_values2=[]


for segnalibro in range(0,len(dict_na4['giocatori'])):
    check=False
    for row in df_agg1.itertuples():

        if (row.Name==dict_na4['giocatori'][segnalibro] and row.Club==dict_na4['squadre_partenza'][segnalibro] and
                 row.ClubInvolved== dict_na4['squadre_arrivo'][segnalibro] and str(row.Età)==str(dict_na4['eta'][segnalibro])):

            #print('ok2')
            lista_transfer_values2.append(row.Costo)
            check=True
            break

        # elif (row.Name==dict_na4['giocatori'][segnalibro] and str(row.Età)==str(dict_na4['eta'][segnalibro])):
        #
        #     #print('ok3')
        #     lista_transfer_values2.append(row.Costo)
        #     check=True
        #     break


    if not check:
        lista_transfer_values2.append('NF')
        #print(dict_na['giocatori'][segnalibro])

print(lista_transfer_values2)
print(len(lista_transfer_values2))

print(len(df_nostro.index))


df_nostro.transfer_value[(df_nostro.transfer_value=='?')|(df_nostro.transfer_value=='-')|(df_nostro.transfer_value=='NF')]=lista_transfer_values2
print(type(df_nostro.transfer_value[0]))

print(df_nostro.transfer_value)

df_nostro.to_csv('dataset_completo11-15.csv')

######################################################################################################################
######################################################################################################################
######################################################################################################################
#CARICAMENTO DATASET
import pandas as pd

df_completo=pd.read_csv('dataset_completo11-15.csv')

#UNIFICAZIONE DIVERSI NOMI PER STESSA SQUADRA:
df_completo['team1'].replace(['FC Internazionale','Inter Milan'],'FC Inter',inplace=True)
df_completo['team2'].replace(['FC Internazionale','Inter Milan'],'FC Inter',inplace=True)
df_completo['team1'].replace(['FC Internazionale Primavera','Inter Milan Primavera'],'FC Inter Primavera',inplace=True)
df_completo['team2'].replace(['FC Internazionale Primavera','Inter Milan Primavera'],'FC Inter Primavera',inplace=True)
df_completo['team1'].replace(['SSC Bari','FC Bari 1908'],'Bari',inplace=True)
df_completo['team2'].replace(['SSC Bari','FC Bari 1908'],'Bari',inplace=True)
df_completo['team1'].replace(['SSC Bari Primavera','FC Bari 1908 Primavera'],'Bari Primavera',inplace=True)
df_completo['team2'].replace(['SSC Bari','FC Bari 1908 Primavera'],'Bari Primavera',inplace=True)
df_completo['team1'].replace(['US Palermo','SSD Palermo'],'Palermo',inplace=True)
df_completo['team2'].replace(['US Palermo','SSD Palermo'],'Palermo',inplace=True)
df_completo['team1'].replace(['US Palermo Primavera','SSD Palermo Primavera'],'Palermo Primavera',inplace=True)
df_completo['team2'].replace(['US Palermo Primavera','SSD Palermo Primavera'],'Palermo Primavera',inplace=True)
df_completo['team1'].replace(['Ascoli Calcio','Ascoli Picchio'],'Ascoli',inplace=True)
df_completo['team2'].replace(['Ascoli Calcio','Ascoli Picchio'],'Ascoli',inplace=True)
df_completo['team1'].replace(['US Salernitana 1919','Salernitana Calcio','Salerno Calcio'],'Salernitana',inplace=True)
df_completo['team2'].replace(['US Salernitana 1919','Salernitana Calcio','Salerno Calcio'],'Salernitana',inplace=True)


#
#


#CONTEGGIO DEL TIPO DI VALORI ALL'INTERNO DI CIASCUNA COLONNA:
for column in df_completo.columns:
    print(column)
    print('numero stringhe', sum([1 for row in df_completo[f'{column}']if type(row)==str]))
    print('numero float', sum([1 for row in df_completo[f'{column}'] if type(row) == float]))
    print('numero interi', sum([1 for row in df_completo[f'{column}'] if type(row) == int]))
    print('numero booleani', sum([1 for row in df_completo[f'{column}'] if type(row) == bool]))

#df_completo_pulito=df_completo[df_completo.market_value!='-']
#print(df_completo_pulito)
#print(df_completo_pulito.market_value)
df_completo['market_value']=df_completo['market_value'].str.replace(r' mln','0000',regex=True)
df_completo['market_value']=df_completo['market_value'].str.replace(r' mila','000',regex=True)
df_completo['market_value']=df_completo['market_value'].str.replace(r'-','0',regex=True)
df_completo['market_value']=df_completo['market_value'].str.replace(r'€','',regex=True)
df_completo['market_value']=df_completo['market_value'].str.replace(r',','',regex=True)
df_completo['market_value']=df_completo['market_value'].str.replace(r' ','',regex=True)

df_completo['transfer_value']=df_completo['transfer_value'].str.replace(r' mln','0000',regex=True)
df_completo['transfer_value']=df_completo['transfer_value'].str.replace(r' mila','000',regex=True)
df_completo['transfer_value']=df_completo['transfer_value'].str.replace(r'-','0',regex=True)
df_completo['transfer_value']=df_completo['transfer_value'].str.replace(r'€','',regex=True)
df_completo['transfer_value']=df_completo['transfer_value'].str.replace(r',','',regex=True)
df_completo['transfer_value']=df_completo['transfer_value'].str.replace(r' ','',regex=True)
#print(df_completo_pulito.market_value)
#df_nostro=df_nostro.astype({'player_age':float})
df_completo_pulito=df_completo[df_completo.market_value!='NF']
df_completo_pulito=df_completo_pulito[(df_completo_pulito.transfer_value!='NF')&(df_completo_pulito.transfer_value!='?')]
df_completo_pulito=df_completo_pulito.astype({'market_value':float})
df_completo_pulito=df_completo_pulito.astype({'transfer_value':float})
df_completo_pulito=df_completo_pulito.astype({'market_value':int})
df_completo_pulito=df_completo_pulito.astype({'transfer_value':int})
# df_completo_pulito
# #
#
# media=int((df_completo_pulito['market_value'].mean()))
# print(media)
#
# df_completo_media=df_completo.replace('-',f'{media}',inplace=False)
# df_completo_media['market_value']=df_completo_media['market_value'].str.replace(r' mln','0000',regex=True)
# df_completo_media['market_value']=df_completo_media['market_value'].str.replace(r' mila','000',regex=True)
# df_completo_media['market_value']=df_completo_media['market_value'].str.replace(r'€','',regex=True)
# df_completo_media['market_value']=df_completo_media['market_value'].str.replace(r',','',regex=True)
# df_completo_media['market_value']=df_completo_media['market_value'].str.replace(r' ','',regex=True)
#
# df_completo_media=df_completo_media.astype({'market_value':int})

df_completo_pulito.to_csv('dataset_pronto10-15.csv')



########################
#CREAZIONE DATASET AGGIUNTIVO CON SQUADRE ITALIANE E LEGA DI MAGGIORE APPARTENENZA




import pandas as pd
df_completo_pulito= pd.read_csv("dataset//dataset_finale10_15pronto.csv")
df_completo_pulitoITA = df_completo_pulito[df_completo_pulito.league_team1.str.startswith("ITA")]
df_completo_pulitoITA_filter = df_completo_pulitoITA.groupby(['team1','league_team1'])['season'].unique().apply(list).reset_index()
df_completo_pulitoITA_filter= pd.DataFrame(data=df_completo_pulitoITA_filter)
df_completo_pulitoITA_filter.to_csv("STEP1", index=False)
df_completo_pulitoITA_filter = pd.read_csv("STEP1")
df_completo_pulitoITA_filter2 = df_completo_pulitoITA_filter.groupby(['team1','league_team1'])["season"].agg(lambda x: x.str.len().max()).reset_index()
df_nostro_sorted = df_completo_pulitoITA_filter2.sort_values(by='season')
df_nostro_sorted = pd.DataFrame(data=df_nostro_sorted)
df_nostro_sorted.to_csv("STEP2.csv")
df_nostro_sorted.drop_duplicates(subset=['team1'],ignore_index=True,inplace=True,keep='last')
df_nostro_sorted.to_csv('dataset_supporto.csv')

