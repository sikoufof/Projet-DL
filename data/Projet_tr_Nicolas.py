#%%
from networkx.algorithms.shortest_paths.weighted import dijkstra_path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
from itertools import combinations
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
price = price.fillna(0)

price.columns = ([0]+list(data_co.NOMGARE))
price.index = list(data_co.NOMGARE)

#price.columns = map(lambda x: str(x).upper(), price.columns)
#a = list(price.iloc[:,0])
#price.index = a
#price.index = map(lambda x: str(x).upper(), price.index)

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

#On garde les routes nous concernant, on supprime donc les autres
dta_routes = dta_routes.drop(0)
dta_routes = dta_routes.drop(1)
dta_routes = dta_routes.drop(2)
dta_routes = dta_routes.drop(3)
dta_routes = dta_routes.drop(5)
dta_routes = dta_routes.drop(6)
dta_routes = dta_routes.drop(7)
dta_routes = dta_routes.drop(18)
dta_routes = dta_routes.drop(31)
dta_routes = dta_routes.drop(32)
dta_routes = dta_routes.drop(33)
dta_routes = dta_routes.drop(34)
dta_routes = dta_routes.drop(35)
# il en reste à supprimer, mais on utilise coordonnées 

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
    '''transforme le nom de la sortie en entier parmis la "liste Sortie" '''
    if a in PP:
        return(a)
    for i in range(len(data_co.NOMGARE)):
        if a == data_co.NOMGARE[i] :
            if a in [5,17,18,32,34]:
                return("Entrée/sortie invalide")
            return(i)
    return("Entrée/sortie invalide")

def re_transforme(a):
    if a in (list(data_co.NOMGARE)):
        return(a)
    for i in range(len(data_co.NOMGARE)):
        b = data_co.NOMGARE[i]
        if a == transforme(b) :
            return(b)
    return("Entrée/sortie invalide")

def id_portion(a):
    '''retourne à quel portion de route appartient l'entier ou le nom de sortie "a" '''
    a = transforme(a)
    for i in range(5):
        if a in P[i][0]:
            return(i)

def position_portion(a):
    '''retourne l'indice de a(entier/nom de sortie) dans la portion de route auquel il appartient'''
    a = transforme(a)
    i_a = id_portion(a)
    for j in range(len(P[i_a][0])):
        if a == P[i_a][0][j]:
            return(j)

def r(L):
    '''renverse une liste'''
    a = [0]*(len(L))
    for i in range(len(L)):
        a[-(i+1)] = L[i]
    return(a)

def chemin(e,s): 
    '''retourne le trajet des sorties (entier dans la "liste sortie") 
    entre l'entré/sortie (entier/ou nom:string)'''
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

    if e ==s:
        return("Vous ne prenez aucun itinéraire")
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

def trajet(e,s,k):
    '''liste de tous les trajets possible en k sorties intermédiares 
    entre l'entré/sortie (e/s sous forme entier/string)'''
    e = transforme(e)
    s = transforme(s)
    L = []
    for i in(combinations(chemin(e,s),k+2)): 
        if list(i)[0]==e and list(i)[-1]==s:
            L.append(list(i))
    return(L)

def cout_direct(e,s):
    '''retourne le coût d'un allé direct entre entré/sortie
    (e/s sous forme int/string)'''
    e = transforme(e)
    s = transforme(s)+1
    prix = price.iloc[e,s]
    return(prix)


def prix_chemin(e,s,k):
    L = trajet(e,s,k)
    long_L = len(L)
    L2 = [0]*long_L
    indice = 0
    prix = 1000
    for i in range(long_L):
        L_c = L[i]
        prix_c = 0
        for j in range(len(L_c)-1):
            prix_c = prix_c + cout_direct(L_c[j],L_c[j+1])
        if prix > prix_c:
            prix = prix_c
            indice = i
        L2[i] = prix_c
    return([L[indice],L2[indice]])



def prixopt(A):
    L=[]
    somm1=1000
    somm2=0
    for i in range(len(A)):
        for j in range(len(A[i])-1):
            somm2+=price.iloc[A[i][j],A[i][j+1]+1]
        if somm2<somm1 :
            somm1=somm2
            somm2=0
            L=A[i]
        else:
            somm2=0
    return [L,somm1]

#%%
def Finale(A,B,k):
    L=[]
    if A==B:
        return "Vous devez choisir une sortie différente de votre point d'entrée"
    for i in range(k+1):
        L.append(prixopt(trajet(A,B,i)))
    a=prixopt(trajet(A,B,0))
    for j in range(len(L)):
        if L[j][1]<a[1]:
            a=L[j]
    a.append(len(a[0])-2)
    return a





def sortie_moins_cher(LB):
    '''LB est une liste de string (chemin)'''
    long_LB = len(LB)
    if (long_LB == 2) | (long_LB == 1) | (long_LB == 0) :
        return("aucune sortie")
    indice = 1
    prix = cout_direct(LB[0],LB[1])
    for i in range(2,long_LB):
        prix_2 = cout_direct(LB[0],LB[i])
        if prix > prix_2:
            prix = prix_2
            indice = i
    return([prix,LB[indice]])



#%%
def chemin_k_sortie(k,e,s):
    ch = chemin(e,s)
    long_ch = len(ch)
    sortie = 0
    if (long_ch == 2) :
        return("faites un allé direct")
    if (long_ch == 1) | (long_ch == 0) :
        return("aucune entré/sortie indiqué")
    prix_compare = [ [], [ [],[] ] ]
    for i in range(1,len(ch)):
        prix_compare[0].append(cout_direct(e,i)[0])
        prix_compare[1][0].append(transforme(cout_direct(e,i)[1]))
        prix_compare[1][1].append(sortie)

def dijkstra(e,s,k):
    ch = chemin(e,s)
    long_ch = len(ch)
    if (long_ch == 2) :
        return("faites un allé direct")
    if (long_ch == 1) | (long_ch == 0) :
        return("aucune entré/sortie indiqué")
    liste_op = [e]
    k_c = k
    n = 0
    chemin_co = chemin(e,s)
    prix = 0
    l_prix = [[0,0]]*k
    while (n!=300) | (k_c != 0) | (len(chemin_co) != 2):
        prix_co,sortie_EV = sortie_moins_cher(chemin_co)
        prix_cu = prix_co + prix
        if prix_cu <= min(l_prix):


        dijkstra_etape(k_c,)
    return(liste_op)


def dijkstra_etape(k,trajet,list_p):

    prix_p = P_S[0][0]
    k_p = k
    if k_p != 0: 
        a = sortie_moins_cher(chemin(P_S[1],s))
        prix_c = a[0]
        prix_cu = prix_p + prix_c
        if prix_cu <= min(P_S[0][1:]):
            k_p = k_p - 1
            up_grade(P_S,prix_cu,)




    a = sortie_moins_cher(list)
    b = sortie_moins_cher(list[a[1]:])#à rectifier 
    prix_mi_tr = a[0]+b[0]
    del a[0][0]

    if prix_mi_tr <= min(a[0]):
        return()
    l = sorted(list)
    p = list[0]
    i = 0
    for i in range(len(l)):
        if p < list[i+1]:

# carte interactive 

