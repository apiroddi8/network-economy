import pandas as pd
from collections import defaultdict

nostro_df= pd.read_csv('prova1.csv')
loro_df=pd.read_csv('df_7_file.csv')





nostro_df.rename(columns = {'league':'league_team1', 'team_name':'team1', 'team_country':'country_team1',
                     'counter_team_name':'team2','counter_team_country':'country_team2',
                     'transfer_fee_amnt':'transfer_value','market_val_amnt':'market_value'}, inplace = True)

####################################################################################################### DA FINIRE
# print(nostro_df[(nostro_df['dir']=='in')& (nostro_df['window']=='s')]['league_team1'])
# #df[(df['A'] == "A") & (df['B'] == "2")]['C']
# #
# lista_colonna_league2=[]
# for row in nostro_df.itertuples():
#     top_countries=['England','Spain','Germany','Portugal','France','Netherlands']
#     if any([row.country_team2 == top_country for top_country in top_countries]):
#         if row.team2 in:
#             lista_colonna_league2.append(row.country_team2[:3].upper())
#         else:
#             lista_colonna_league2.append(row.country_team2[:3]+'2'.upper())
#
#     elif row.country_team2=='Italy':
#         if row.dir=='left':
#             nostro_df.loc[nostro_df['dir']=='in'and nostro_df['transfer_id']==row.transfer_id]['league_team1']
#     else:
#         lista_colonna_league2.append(row.country_team2[:3].upper())

####################################################################################################################


print('CONTEGGIO NA PRE PULIZIA\n')

for column in nostro_df.columns:
    print(column,nostro_df[f'{column}'].isna().sum())

nostro_df.drop(columns=['player_nation2','team_id','counter_team_id'],inplace=True,axis=1)
nostro_df.dropna(subset=['player_age','player_nation','country_team2','transfer_id'],inplace=True)

print(nostro_df.player_pos.unique())

nostro_df['player_pos'].replace(['GK'],'goalkeeper',inplace=True)
nostro_df['player_pos'].replace(['RB','CB','LB','defence'],'defender',inplace=True)
nostro_df['player_pos'].replace(['CM','AM','DM','LM','RM','midfield'],'midfielder',inplace=True)
nostro_df['player_pos'].replace(['CF','SS','LW','RW','attack'],'striker',inplace=True)



#nostro_df['age_cat'] = pd.cut(df['age'], bins=[0,23,54,56, 999], labels=['Young', 'Adult', 'Elder','other'])

print('CONTEGGIO NA POST PULIZIA \n')

for column in nostro_df.columns:
    print(column,nostro_df[f'{column}'].isna().sum())

nostro_df=nostro_df.astype({'player_age':float})
nostro_df=nostro_df.astype({'player_age':int})

for column in nostro_df.columns:
    print(column)
    print('numero stringhe', sum([1 for row in nostro_df[f'{column}']if type(row)==str]))
    print('numero float', sum([1 for row in nostro_df[f'{column}'] if type(row) == float]))
    print('numero interi', sum([1 for row in nostro_df[f'{column}'] if type(row) == int]))
    print('numero booleani', sum([1 for row in nostro_df[f'{column}'] if type(row) == bool]))


dict_na=defaultdict(list)

for row in nostro_df[nostro_df['market_value'].isna()].itertuples():

    if row.dir=='left':
        dict_na['giocatori'].append(row.player_name)
        dict_na['squadre_partenza'].append(row.team1)
        dict_na['squadre_arrivo'].append((row.team2))
        dict_na['eta'].append(row.player_age)

    elif row.dir=='in':
        dict_na['giocatori'].append(row.player_name)
        dict_na['squadre_partenza'].append(row.team2)
        dict_na['squadre_arrivo'].append(row.team1)
        dict_na['eta'].append(row.player_age)

lista_market_values=[]

for segnalibro in range(0,len(dict_na['giocatori'])):
    check=False
    for row in loro_df.itertuples():

        if (row.Name==dict_na['giocatori'][segnalibro]) and ((row.Club==dict_na['squadre_partenza'][segnalibro] and
                 row.ClubInvolved== dict_na['squadre_arrivo'[segnalibro]]) or str(row.Età)==str(dict_na['eta'][segnalibro])):

            print('ok')
            lista_market_values.append(row.MarketValue)
            check=True
            break

    if not check:
        lista_market_values.append('NA')
        print(dict_na['giocatori'][segnalibro])

print(lista_market_values)
print(len(lista_market_values))

print(nostro_df.player_pos)

#nostro_df.loc[pd.isnull(df['A']), 'A'] = mylist
nostro_df.loc[pd.isnull(nostro_df['market_value']),'market_value']=lista_market_values