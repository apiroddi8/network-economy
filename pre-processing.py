import pandas as pd
from collections import defaultdict
#
#CARICAMENTO DATASET:
nostro_df= pd.read_csv('transfers (1).csv')
loro_df=pd.read_csv('df_7_file.csv')
nostro_df_pulito=pd.read_csv('nostro_df_pulito.csv')
# #
#RINOMINAZIONE COLONNE:
nostro_df.rename(columns = {'league':'league_team1', 'team_name':'team1', 'team_country':'country_team1',
                     'counter_team_name':'team2','counter_team_country':'country_team2',
                     'transfer_fee_amnt':'transfer_value','market_val_amnt':'market_value'}, inplace = True)

#print(nostro_df.to_string())
print(len(nostro_df.index))

print('##########################################')

#RINOMINAZIONE VALORI COLONNA LEGHE:
nostro_df['league_team1'].replace('IT1','ITA1',inplace=True)
nostro_df['league_team1'].replace('IT2','ITA2',inplace=True)
nostro_df['league_team1'].replace('ES1','SPA1',inplace=True)
nostro_df['league_team1'].replace('GB1','ENG1',inplace=True)
nostro_df['league_team1'].replace('L1','GER1',inplace=True)
nostro_df['league_team1'].replace('FR1','FRA1',inplace=True)
nostro_df['league_team1'].replace('PO1','POR1',inplace=True)
nostro_df['league_team1'].replace('NL1','NED1',inplace=True)

#print(nostro_df.to_string())
print(len(nostro_df.index))

print('################################################')

#CREAZIONE DELLA COLONNA CHE CONTIENE LA LEGA DI APPARTENENZA DEL TEAM 2
#IL DATASET INIZIALMENTE HA SOLTANTO LA COLONNA DELLA LEGA DI APPARTENENZA DEL TEAM 1:
lista_colonna_league2=[]

for row in nostro_df.itertuples():
    top_countries=['England','Spain','Germany','Portugal','France','Netherlands']
    if any([row.country_team2 == top_country for top_country in top_countries]):
        if row.team2 in set(list(nostro_df[(nostro_df['league_team1']==row.country_team2[:3].upper()+'1') & (nostro_df['season']==row.season)]['team1'])):
            lista_colonna_league2.append(row.country_team2[:3].upper()+'1')
        else:
            lista_colonna_league2.append(row.country_team2[:3].upper()+'2')

    elif row.country_team2=='Italy':

        if row.dir=='left' and len(list(nostro_df[(nostro_df['dir'] == 'in') & (nostro_df['team1'] == row.team2)]['league_team1']))>0:
            lista_colonna_league2.append(list(nostro_df[(nostro_df['dir'] == 'in') & (nostro_df['team1'] == row.team2)]['league_team1'])[0])######
        elif row.dir=='in' and len(list(nostro_df[(nostro_df['dir']=='left') & (nostro_df['team1']==row.team2)]['league_team1']))>0:
            lista_colonna_league2.append(list(nostro_df[(nostro_df['dir']=='left') & (nostro_df['team1']==row.team2)]['league_team1'])[0])########
        else:
            lista_colonna_league2.append(row.country_team2[:3].upper()+'4')
    else:
        lista_colonna_league2.append(row.country_team2[:3].upper())


print('########################')
#print(lista_colonna_league2)
print('#######################')

nostro_df['league_team2']=lista_colonna_league2

#print(nostro_df.to_string())
print(len(nostro_df.index))

print('###########################')




#ELIMINAZIONE TRANSFER ID DUPLICATI, RESTANO SOLO I LEFT:
nostro_df.drop_duplicates(subset='transfer_id',ignore_index=True,inplace=True)

#print(nostro_df.to_string())
print(len(nostro_df.index))

condition = nostro_df['dir'] == 'in'

nostro_df.loc[condition, ['team1', 'team2']] = (
    nostro_df.loc[condition, ['team2', 'team1']].values)

nostro_df.loc[condition, ['country_team1', 'country_team2']] = (
    nostro_df.loc[condition, ['country_team2', 'country_team1']].values)

nostro_df.loc[condition, ['league_team1', 'league_team2']] = (
    nostro_df.loc[condition, ['league_team2', 'league_team1']].values)

# print(nostro_df.team1)
# print(nostro_df.team2)
# print(nostro_df.country_team1)
# print(nostro_df.country_team2)

nostro_df['dir'].replace(['in'],'left',inplace=True)

#print(nostro_df.to_string())
print(len(nostro_df.index))

# nostro_df2=nostro_df.drop_duplicates(subset=['team1','season','window','player_name','team2'],ignore_index=True,inplace=False)
#
# #print(nostro_df.to_string())
# print(len(nostro_df2.index))
#
# print(nostro_df[~nostro_df.apply(tuple,1).isin(nostro_df2.apply(tuple,1))])




#CHECK, PER OGNI STAGIONE, CHE TUTTE LE SQUADRE DEL CAMPIONATO SIANO PRESENTI:
print(len(set(list(nostro_df[(nostro_df['league_team1']=='PO1') & (nostro_df['season']==2021)]['team1']))))
print(len(set(list(nostro_df[(nostro_df['league_team1']=='PO1') & (nostro_df['season']==2020)]['team1']))))
print(len(set(list(nostro_df[(nostro_df['league_team1']=='PO1') & (nostro_df['season']==2019)]['team1']))))
print(len(set(list(nostro_df[(nostro_df['league_team1']=='PO1') & (nostro_df['season']==2018)]['team1']))))
print(len(set(list(nostro_df[(nostro_df['league_team1']=='PO1') & (nostro_df['season']==2017)]['team1']))))
print(len(set(list(nostro_df[(nostro_df['league_team1']=='PO1') & (nostro_df['season']==2016)]['team1']))))
print(len(set(list(nostro_df[(nostro_df['league_team1']=='PO1') & (nostro_df['season']==2015)]['team1']))))
print(len(set(list(nostro_df[(nostro_df['league_team1']=='PO1') & (nostro_df['season']==2014)]['team1']))))
print(len(set(list(nostro_df[(nostro_df['league_team1']=='PO1') & (nostro_df['season']==2013)]['team1']))))
print(len(set(list(nostro_df[(nostro_df['league_team1']=='PO1') & (nostro_df['season']==2012)]['team1']))))
print(len(set(list(nostro_df[(nostro_df['league_team1']=='PO1') & (nostro_df['season']==2011)]['team1']))))
print(len(set(list(nostro_df[(nostro_df['league_team1']=='PO1') & (nostro_df['season']==2010)]['team1']))))
print(len(set(list(nostro_df[(nostro_df['league_team1']=='PO1') & (nostro_df['season']==2009)]['team1']))))


#CONTEGGIO NA DELLE VARIE COLONNE PRIMA DELLA PULIZIA:
print('CONTEGGIO NA PRE PULIZIA\n')

for column in nostro_df.columns:
    print(column,nostro_df[f'{column}'].isna().sum())

#ELIMINAZIONE COLONNE INUTILI:
nostro_df.drop(columns=['player_nation2','team_id','counter_team_id'],inplace=True,axis=1)
#print(nostro_df.to_string())

#ELIMINAZIONE DEGLI NA CHE RAPPRESENTANO UNA PARTE NON SIGNIFICATIVA DEL TOTALE DELLE OSSERVAZIONI:
nostro_df.dropna(subset=['player_age','player_nation','country_team2','transfer_id'],inplace=True)
#print(nostro_df.to_string())

#OTTENIMENTO DELLA LISTA DI TUTTI I RUOLI DI TRANSFERMARKT (PRESI UNA SOLA VOLTA):
print(nostro_df.player_pos.unique())

#UNIFICAZIONE DIVERSI NOMI PER STESSA SQUADRA:
nostro_df['team1'].replace(['FC Internazionale','Inter Milan'],'FC Inter',inplace=True)
nostro_df['team2'].replace(['FC Internazionale','Inter Milan'],'Fc Inter',inplace=True)
nostro_df['team1'].replace(['SSC Bari','FC Bari 1908'],'Bari',inplace=True)
nostro_df['team2'].replace(['SSC Bari','FC Bari 1908'],'Bari',inplace=True)
nostro_df['team1'].replace(['US Palermo','SSD Palermo'],'FC Inter',inplace=True)
nostro_df['team2'].replace(['US Palermo','SSD Palermo'],'Fc Inter',inplace=True)

#ACCORPAMENTO DEI VARI RUOLI NELLE 4 MACROCATEGORIE: PORTIERE, DIFENSORE, CENTROCAMPISTA, ATTACCANTE:
nostro_df['player_pos'].replace(['GK'],'goalkeeper',inplace=True)
nostro_df['player_pos'].replace(['RB','CB','LB','defence'],'defender',inplace=True)
nostro_df['player_pos'].replace(['CM','AM','DM','LM','RM','midfield'],'midfielder',inplace=True)
nostro_df['player_pos'].replace(['CF','SS','LW','RW','attack'],'striker',inplace=True)
#nostro_df['age_cat'] = pd.cut(df['age'], bins=[0,23,54,56, 999], labels=['Young', 'Adult', 'Elder','other'])
#print(nostro_df.to_string())

#ASSEGNAZIONE DEL VALORE ZERO AL VALORE DEL TRASFERIMENTO QUANDO IS FREE= TRUE; IS END LOAN= TRUE, TEAM2=WITHOUT CLUB:
nostro_df.loc[(nostro_df['is_loan_end'] == True) | (nostro_df['is_free']==True) | (nostro_df['team2']=='Without Club'), 'transfer_value'] = 0.0

#print(nostro_df.to_string())
#
# #CONTEGGIO DEGLI NA UNA VOLTA TERMINATA LA PULIZIA:
print('CONTEGGIO NA POST PULIZIA \n')

for column in nostro_df.columns:
    print(column,nostro_df[f'{column}'].isna().sum())
#
#
# #LA COLONNA DELL'ETA HA VALORI DI TIPO STRINGA, DOVREBBERO ESSERE INVECE NUEMERICI
# #CONVERTIAMO TUTTI I VALORI DELLA COLONNA ETA PRIMA IN FLOAT E POI IN INTERI:
nostro_df=nostro_df.astype({'player_age':float})
nostro_df=nostro_df.astype({'player_age':int})

#print(nostro_df.to_string())

#CONTEGGIO DEL TIPO DI VALORI ALL'INTERNO DI CIASCUNA COLONNA:
for column in nostro_df.columns:
    print(column)
    print('numero stringhe', sum([1 for row in nostro_df[f'{column}']if type(row)==str]))
    print('numero float', sum([1 for row in nostro_df[f'{column}'] if type(row) == float]))
    print('numero interi', sum([1 for row in nostro_df[f'{column}'] if type(row) == int]))
    print('numero booleani', sum([1 for row in nostro_df[f'{column}'] if type(row) == bool]))


#OTTENIMENTO DEI VALORI MANCANTI DEL MARKET VALUE ANDANDOLI A PESCARE DAL DATASET DEI COLLEGHI CAGLIARITANI:
dict_na={}

dict_na['giocatori']=nostro_df['player_name'].tolist()
dict_na['squadre_partenza']=nostro_df['team1'].tolist()
dict_na['squadre_arrivo']=nostro_df['team2'].tolist()
dict_na['eta']=nostro_df['player_age'].tolist()

print(dict_na)



lista_market_values=[]


for segnalibro in range(0,len(dict_na['giocatori'])):
    check=False
    for row in loro_df.itertuples():

        if (row.Name==dict_na['giocatori'][segnalibro]) and ((row.Club==dict_na['squadre_partenza'][segnalibro] and
                 row.ClubInvolved== dict_na['squadre_arrivo'][segnalibro]) or str(row.Età)==str(dict_na['eta'][segnalibro])):

            print('ok')
            lista_market_values.append(row.MarketValue)
            check=True
            break

    if not check:
        lista_market_values.append('-')
        #print(dict_na['giocatori'][segnalibro])

print(lista_market_values)
print(len(lista_market_values))

print(len(nostro_df.index))
print(type(nostro_df.market_value[0]))
nostro_df['market_value']=lista_market_values

print(nostro_df.market_value)





#nostro_df.loc[pd.isnull(df['A']), 'A'] = mylist
#nostro_df.loc[pd.isnull(nostro_df['market_value']),'market_value']=lista_market_values


#OTTENIMENTO DEI VALORI MANCANTI DEL TRANSFER VALUE ANDANDOLI A PESCARE DAL DATASET DEI COLLEGHI CAGLIARITANI:

lista_transfer_values=[]

for segnalibro in range(0,len(dict_na['giocatori'])):
    check=False
    for row in loro_df.itertuples():

        if (row.Name==dict_na['giocatori'][segnalibro]) and ((row.Club==dict_na['squadre_partenza'][segnalibro] and
                 row.ClubInvolved== dict_na['squadre_arrivo'[segnalibro]]) or str(row.Età)==str(dict_na['eta'][segnalibro])):

            print('ok')
            lista_transfer_values.append(row.Costo)
            check=True
            break

    if not check:
        lista_transfer_values.append('-')
        #print(dict_na['giocatori'][segnalibro])

print(lista_transfer_values)
print(len(lista_transfer_values))

print(len(nostro_df.index))
print(type(nostro_df.transfer_value[0]))
nostro_df['transfer_value']=lista_transfer_values

print(nostro_df.transfer_value)

nostro_df.to_csv('nostro_df_pulito.csv')



# #CONTEGGIO DEL TIPO DI VALORI ALL'INTERNO DI CIASCUNA COLONNA:
for column in nostro_df_pulito.columns:
    print(column)
    print('numero stringhe', sum([1 for row in nostro_df_pulito[f'{column}']if type(row)==str]))
    print('numero float', sum([1 for row in nostro_df_pulito[f'{column}'] if type(row) == float]))
    print('numero interi', sum([1 for row in nostro_df_pulito[f'{column}'] if type(row) == int]))
    print('numero booleani', sum([1 for row in nostro_df_pulito[f'{column}'] if type(row) == bool]))

nostro_df_pulito_trattini=nostro_df_pulito[nostro_df_pulito.market_value!='-']
print(nostro_df_pulito_trattini)
#print(nostro_df_pulito_trattini.market_value)
nostro_df_pulito_trattini['market_value']=nostro_df_pulito_trattini['market_value'].str.replace(r' mln','0000',regex=True)
nostro_df_pulito_trattini['market_value']=nostro_df_pulito_trattini['market_value'].str.replace(r' mila','000',regex=True)
nostro_df_pulito_trattini['market_value']=nostro_df_pulito_trattini['market_value'].str.replace(r'€','',regex=True)
nostro_df_pulito_trattini['market_value']=nostro_df_pulito_trattini['market_value'].str.replace(r',','',regex=True)
nostro_df_pulito_trattini['market_value']=nostro_df_pulito_trattini['market_value'].str.replace(r' ','',regex=True)
print(nostro_df_pulito_trattini.market_value)
#nostro_df=nostro_df.astype({'player_age':float})
nostro_df_pulito_trattini=nostro_df_pulito_trattini.astype({'market_value':int})
#

media=int((nostro_df_pulito_trattini['market_value'].mean()))
print(media)

nostro_df_pulito_media=nostro_df_pulito.replace('-',f'{media}',inplace=False)
nostro_df_pulito_media['market_value']=nostro_df_pulito_media['market_value'].str.replace(r' mln','0000',regex=True)
nostro_df_pulito_media['market_value']=nostro_df_pulito_media['market_value'].str.replace(r' mila','000',regex=True)
nostro_df_pulito_media['market_value']=nostro_df_pulito_media['market_value'].str.replace(r'€','',regex=True)
nostro_df_pulito_media['market_value']=nostro_df_pulito_media['market_value'].str.replace(r',','',regex=True)
nostro_df_pulito_media['market_value']=nostro_df_pulito_media['market_value'].str.replace(r' ','',regex=True)

nostro_df_pulito_media=nostro_df_pulito_media.astype({'market_value':int})

nostro_df_pulito_media.to_csv('nostro_df_pulito_media.csv')