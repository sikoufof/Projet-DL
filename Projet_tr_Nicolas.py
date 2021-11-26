#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from functools import partial
from pyproj import CRS
from pyproj import Proj, transform
# widget manipulation
from ipywidgets import widgets, interact, interactive, fixed, interact_manual

from download import download  # download data / avoid re-downloading
from IPython import get_ipython

pd.options.display.max_rows = 8
#%%

#Importation de la dataset 
#%%
Jdd_projet = pd.read_csv("gares-peage-2019.csv", sep = ';', header = 0)
Jdd_projet 



Coordonnees = pd.read_csv("coordonnees.csv", sep = ';', header = 0)
Coordonnees









#%%
#énumération des colonnes
#%%

print(Jdd_projet.columns)

#%%

#displaying the first five rows of dataset 
#%%
print(Jdd_projet.head())
#%%
#descrition of data
#%%
print(Jdd_projet.describe(include = 'all'))
print(Jdd_projet.info())
#%%
#displayinf last five rows of dataset
#%%
print(Jdd_projet.tail())
#%%
# read the data null
#%%
print(Jdd_projet.isnull())
#%%
#Utilisation de la fonction isna()
#%%
print(Jdd_projet.isna())
print(Jdd_projet.isna().any())

#Cette fonction donne la somme des valeurs nulls dans le jeu de données
#%%
Jdd_projet.isna().sum()
#%%
# Faire une liste de types de valeurs manquantes
#%%
missing_values = ["n/a", "na", "--"]
Jdd_projet = pd.read_csv("gares-peage-2019.csv", sep = ';', header = 0, na_values = missing_values)
Jdd_projet
#%%
#Suppression des valeurs manquantes

#%%
Jdd_projet = Jdd_projet.dropna()
Jdd_projet
print(Jdd_projet.isnull())
#%%
# Calcul des distances 

#%%
#Conversion des valeurs 
#%%
#X1=Jdd_projet['x']
#X2=Jdd_projet['y']

inProj = Proj("epsg:2154")
outProj = Proj("epsg:4326")
crs_deprecated = CRS("epsg:2154")
crs = CRS("epsg:2154")
crs == crs_deprecated



T= 671659,72
P= 6900724,84
x2,y2 = transform(inProj,outProj,T,P)
print(x2,y2)
x2
y2

#%%