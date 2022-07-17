
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = "https://www.transfermarkt.it/serie-a/ewigeTabelle/wettbewerb/IT1/plus/?saison_id_von=2006&saison_id_bis=2021&tabellenart=alle"
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

team = []
clubs = pageSoup.find_all('td', {'class': 'hauptlink no-border-links'})
point = []
points = pageSoup.find_all('td', {'class': 'rechts hauptlink'})

for tags in clubs:
    team.append(tags.text)
for p in points:
    point.append(p.text)

df = pd.DataFrame(list(zip(team, point)),
               columns =['team', 'point'])

for index, row in df.iterrows():
     df.at[index, 'league'] = "ITA1"

cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]

df.to_csv("squadre_per_fascia/squadre_ita_eterne.csv", index = False)


