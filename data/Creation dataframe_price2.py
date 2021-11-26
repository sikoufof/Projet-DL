#%%
import os
from download import download
import pandas as pd

#%%
# téléchargement du fichier construit par Abdelmalek
price = pd.read_csv("DataFrame_price.csv", sep=';')
price.info()

#%%
# Nettoyage
#Suppression des gares qui ne nous intéressent pas
del price['Vendargues']
del price['Montpellier est']
del price['Montpellier sud']
del price['Le Boulou (peage sys ouvert)']
del price['Montpellier ouest']
del price['St-Jean-de-Vedas']
del price['La Croix Daurade']
del price['Borderouge']
del price['Les lzards']
del price['Sesquieres']
del price['Montaudran']
del price['Lasbordes']
del price['Soupetrad']
del price['La Roseraie']
del price['Pamiers nord']
del price['Pamiers sud']
del price['Montgiscard']
del price['Le palays']
del price['Frontiere Espagnole']
del price['Peage de Toulouse sud/est']
price = price.drop(index=[0, 1, 2, 3, 4, 18, 19, 29, 30, 31,
                        33, 34, 35, 36, 37, 38, 39, 40, 41, 42])
price.set_index(' ', inplace=True)

# Correction pour une seule donnée
price = price.fillna(0)
#%%
price.to_csv('DataFrame_price2.csv')