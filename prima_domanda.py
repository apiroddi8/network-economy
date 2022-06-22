# 1)Tenendo conto di una soglia minima di valore del giocatore al momento del
# trasferimento, quali sono le squadre che nel campionato italiano
# più vengono coinvolte nella circolazione in entrata dei calciatori?
#     dal dataset selezionare solo la lega it1 -> dalla colonna dei trasferimenti selezionare solo il valore in
# Esiste una tendenza da parte della cerchia ristretta di top club a depredare
# le squadre di fasce più basse all’interno del medesimo campionato,
# è possibile individuare un accentramento di tutti gli acquisti rilevanti
# verso queste squadre? Quante sono? [confronto con altri paesi]

#NODI = squadre
#ARCHI = valore trasferimento esclusa soglia minima

import plotly.graph_objects as go
import networkx as nx


