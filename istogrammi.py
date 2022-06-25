import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import seaborn as sns

#lettura file csv
df = pd.read_csv('dataset//nostro_df_pulito.csv')



# ISTOGRAMMA creazione istogramma numero acquisti per lega
df1 = df[df.league_team2.str.endswith("1")]
trasferimenti = df1.groupby(['league_team2']).size().plot(kind='bar',
                                                          color=sns.cubehelix_palette(start=2.8, rot=.1))
plt.title('Acquisti per lega')
plt.xlabel('leghe')
plt.ylabel('trasferimenti')
plt.xticks(rotation=0)


#ISTOGRAMMA valore acquisti per lega
dataset = df[df.league_team2.str.endswith("1")]
fig, ax = plt.subplots()
valore_trasferimenti = dataset.groupby(["league_team2"]).transfer_value.sum().plot(kind="bar",
                                                                                   ax=ax,
                                                                                   color=sns.cubehelix_palette(rot=-.4))
scale_y = 1e6
ticks_y = ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x/scale_y))
ax.yaxis.set_major_formatter(ticks_y)
plt.xlabel('leghe')
plt.ylabel('val trasferimenti(in miliardi)')
plt.xticks(rotation=0)
plt.title('Valore trasferimenti per lega')

plt.show()

#TORTA totale valore acquisti per lega (percentuale)
plt.style.use('ggplot')
df = df.reindex(sorted(df.columns), axis=1)
tot_transfer_value_team2 = df[df.league_team2.str.endswith("1")].transfer_value.sum()

df_filter2= df[df.league_team2.str.endswith("1")]
dff2 = df_filter2.groupby(["league_team2"]).transfer_value.sum().reset_index()

dff2.groupby(['league_team2']).sum().plot(kind='pie',
                                          autopct='%1.0f%%', subplots=True,
                                          title='Acquisti delle diverse leghe',
                                          legend=None)
plt.ylabel(None)
plt.show()
#percentuale = dff2.iloc[:, 1]/tot_transfer_value_team2 * 100












