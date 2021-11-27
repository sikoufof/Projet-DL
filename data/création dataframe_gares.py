#%%
import pandas as pd
import os
from download import download
from pyproj import Proj, transform
#%%

# Le code que nous avons à travers le lien que nous vous avez envoyé
# 
#%%
inProj = Proj(init='epsg:2154')
outProj = Proj(init='epsg:4326')
gares = pd.read_csv('gares-peage-2019.csv', sep=';',usecols=["route", "x", "y", ' Nom gare '],index_col=' Nom gare ', decimal=",")
#%%

# Selection des lignes que nous avons besoin
#%%
coordonnees = gares[(gares['route'] == 'A0009') |
(gares['route'] == 'A0061') |
(gares['route'] == 'A0062') |
(gares['route'] == 'A0075') |
(gares['route'] == 'A0066')]
coordonnees
#%%

# Transformation en coordonées GPS
#%%
x = coordonnees['x'].tolist()
y = coordonnees['y'].tolist()
coordonnees['Long'], coordonnees['Latt'] = transform(inProj, outProj, x, y)
del coordonnees['x'], coordonnees['y']
coordonnees.to_csv('data_loca.csv')

#%%