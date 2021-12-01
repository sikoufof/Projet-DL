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
#La colonne : Nom gare a été remplacé par NomGare dans le csv de base, y'a des espaces qui traines
dta1 = pd.read_csv("gares-peage-2019.csv", sep = ';')
dta1.rename({' NomGare ':'NomGare'},axis=1,inplace=True)

data_co = pd.read_csv("coordonnees.csv", sep = ',')

price = pd.read_csv("DataFrame_price.csv", sep=';')
price.info()

#%%
# Création du tableau des prix 

#Nettoyage de la base de données
#Suppression des gares qui ne nous intéressent pas c'est à dire celles qui n'ont pas de péage
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
#Création de la base de données finale qui contient le prix des péages que nous avons retenus
price.to_csv('DataFrame_price2.csv')

#%%

#Création du tableau des distances

#il doit y avoir une valeur x et y dans le csv sous forme de string:'2' à la place de seulement 2, ex dta1.loc[0,'x']='2'
for i in range(len(dta1.index)):
    dta1.loc[i,'x']=float(dta1.loc[i,'x'].replace(',','.'))
    dta1.loc[i,'y']=float(dta1.loc[i,'y'].replace(',','.'))

#Extraction des données relatives aux autoroutes A9, A709, A61, A62, A75 et A66
dta_routes = dta1[(dta1.route=="A0009")|(dta1.route=="A0709")|(dta1.route=="A0061")|(dta1.route=="A0062")|(dta1.route=="A0075")|(dta1.route=="A0066")]  
dta_routes = dta_routes[['route','NomGare','x','y']]
# a été rectifié : dta_routes= dta_routes.iloc[:,[1,13,7,8]] #pb sur dta1.Nom gare / dta1['Nom gare'] / dta1[['Nom gare']]

# reafections des indices
dta_routes.reset_index(drop = True, inplace = True)
dta_routes

#transformation des coordonnées Lambert93 en coordonéees GPS
from pyproj import Proj, transform

inProj = Proj(init='epsg:2154')
outProj = Proj(init='epsg:4326')
x1= 702805
y1 = 6230817.3
x2,y2 = transform(inProj,outProj,x1,y1)
print(x2,y2)
702805,6230817

X = dta_routes['x']
Y = dta_routes['y']
inProj = Proj(init='epsg:2154')
outProj = Proj(init='epsg:4326')
GPS=[]
GPS_x=[]
GPS_y=[]
for i in range(len(dta_routes.index)):
    GPS.append(transform(inProj,outProj,X[i],Y[i]))
GPS
for i in range(len(GPS)):
    dta_routes.loc[i,'x'],dta_routes.loc[i,'y']=GPS[i]
dta_routes

#Transformation en fichier .csv
dta_routes.to_csv('routes.csv', sep = ';')



#Créations des portions de routes en 5.
Sorties=[0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,19,
20,21,22,23,24,25,26,27,29,30,31,33,35,36,37,38,39,40,
41,42]
P1 = [[0,1,2,3,4,6,7,8,9,10,11],[2,3],[]]
P2 = [[12,13,14,15,16,19],[],[1,3]]
P3 = [[20,21,22,23,24,25],[4,5],[1,2]]
P4 = [[26,27,28,29,30],[],[3,5]]
P5 = [[31,33,35,36,37,38,39,40,41,42],[],[3,4]]
P=[P1,P2,P3,P4,P5]
PP = P1[0]+P2[0]+P3[0]+P4[0]+P5[0]

def transforme(a):
    if a in PP:
        return(a)
    for i in range(len(data_co.NOMGARE)):
        if a == data_co.NOMGARE[i] :
            if a in [5,17,18,32,34]:
                return("Entrée/sortie invalide")
            return(i)
    return("Entrée/sortie invalide")

def transforme_nom(a):
    


def id_portion(a):
    a = transforme(a)
    for i in range(5):
        if a in P[i][0]:
            return(i)

def position_portion(a):
    a = transforme(a)
    i_a = id_portion(a)
    for j in range(len(P[i_a][0])):
        if a == P[i_a][0][j]:
            return(j)

def r(L):
    a = [0]*(len(L))
    for i in range(len(L)):
        a[-(i+1)] = L[i]
    return(a)

def chemin(e,s):
    e = transforme(e)
    s = transforme(s)
    i_e = id_portion(e)
    i_s = id_portion(s)
    min_pe = position_portion(min(P[i_e][0])) # = 0
    max_pe = position_portion(max(P[i_e][0]))
    min_ps = position_portion(min(P[i_s][0])) # = 0
    max_ps = position_portion(max(P[i_s][0]))
    pp_e = position_portion(e)
    pp_s = position_portion(s)

    if (e == 29 and s == 30):
        return("Itinéraire impossible")
    if (e == 30 and s == 29):
        return("Itinéraire impossible")
    if i_e == i_s:
        if e < s:
            return(P[i_e][0][pp_e:pp_s+1])
        return( r(P[i_e][0][pp_s:pp_e+1]) )

    if (i_e+1 in P[i_s][2]) :
        if (i_e == 1) | (i_e == 4)| (i_e ==2 and i_s==1):
            return(r(P[i_e][0][min_pe:pp_e+1])+P[i_s][0][min_ps:pp_s+1])
        return(P[i_e][0][pp_e:max_pe+1]+P[i_s][0][min_ps:pp_s+1])

    if (i_e+1 in P[i_s][1]) :
        if (i_s == 1)|(i_s == 3) :
            return( r(P[i_e][0][min_pe:pp_e+1]) + (P[i_s][0][min_ps:pp_s+1]) )
        return( r(P[i_e][0][min_pe:pp_e+1]) + r(P[i_s][0][pp_s:max_ps+1]) )

    if e < s:
        if (i_e == 1) :
            return( r(P[i_e][0][min_pe:pp_e+1]) + P[2][0] +P[i_s][0][min_ps:pp_s+1])
        else :
            return(P[i_e][0][pp_e:max_pe+1]+ P[2][0] +P[i_s][0][min_ps:pp_s+1])
    else :
        if (i_s == 1) :
            return( r(P[i_e][0][min_pe:pp_e+1]) + r(P[2][0]) + P[i_s][0][min_ps:pp_s+1])
        else :
            return( r(P[i_e][0][min_pe:pp_e+1]) + r(P[2][0]) + r(P[i_s][0][pp_s:max_ps+1]))


def cout(e,s):
    chemin = chemin(e,s)
    prix = [0]*(len(chemin))

VENDARGUES
BRAM

def MoinsCherChemin(e,s):
    chemin = chemin(e,s)
    for 















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
