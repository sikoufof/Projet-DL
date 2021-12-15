import numpy as np
import pandas as pd
import itertools
import folium 
import openrouteservice 
import json
import sys 
import os

from os import replace
from openrouteservice import convert
from itertools import combinations
from ipywidgets import widgets, interact, interactive, fixed, interact_manual
from download import download

#%%
url = 'https://raw.githubusercontent.com/nicolas0344/Projet-DL/main/data/Data_price.csv'
path_tarjet = "./price.csv"
download(url, path_tarjet)
price = pd.read_csv('price.csv', sep=',')
del price['Unnamed: 0']
price.index = price.columns

url = 'https://raw.githubusercontent.com/nicolas0344/Projet-DL/main/data/coordonnees.csv'
path_tarjet = "./sorties.csv"
download(url, path_tarjet)
data_co = pd.read_csv('sorties.csv', sep=',')
del data_co['index']

#%%
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
    min_pe = position_portion(min(P[i_e][0])) 
    # = 0
    max_pe = position_portion(max(P[i_e][0]))
    min_ps = position_portion(min(P[i_s][0])) 
    # = 0
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
    s = transforme(s)
    prix = float(price.iloc[e,s]) # les éléments du tableau price sont des numpy.float et non des float 
    return(prix)


def chemin_k_sortie(e,s,k):
    '''retoune le trajet le moins cher pour exactement k sorties intermédiare, (e/s : str, k : int)'''
    e = transforme(e)
    s = transforme(s)
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

def chemin_opt(e,s,k):
    '''retourne le meilleur trajet pour k sorties autorisées (e/s :str, k:int)'''
    if e==s:
        return("Vous devez choisir une sortie différente de votre point d'entrée")
    opt = chemin_k_sortie(e,s,0)
    for i in range(1,k+1):
        opt_c = chemin_k_sortie(e,s,i)
        if opt_c[1] < opt[1]:
            opt = opt_c 
    for i in range(len(opt[0])):
        opt[0][i] = re_transforme(opt[0][i])
    return(opt)

def nb_sortie_possible(e,s):
    return(len(chemin(e,s))-2)


# carte interactive (Classe Graph)

class Graph(object):
    '''Classe de graphique'''
    def __init__(self):
        pass

    def carte(self,DEPART,ARRIVEE):
        '''retourne la carte d'un trajet (DEPART/ARRIVEE : str)'''

        client = openrouteservice.Client(key='5b3ce3597851110001cf62486f5564a064e34f3895221e5a0d9a2405')
    
        ligne_DEPART = data_co[data_co.NOMGARE == DEPART].index[0]
        ligne_ARRIVEE = data_co[data_co.NOMGARE == ARRIVEE].index[0]

        x = [data_co.loc[ligne_DEPART,'X'],data_co.loc[ligne_ARRIVEE,'X']]
        y = [data_co.loc[ligne_DEPART,'Y'],data_co.loc[ligne_ARRIVEE,'Y']]
    
        m = folium.Map(
            location=[43.1838000,3.0050000],
            zoom_start=10, 
            control_scale=True)

        coords  = (x[0],y[0]),(x[1],y[1])
        res = client.directions(coords)

        geometry = client.directions(coords)['routes'][0]['geometry'] 
        decoded = convert.decode_polyline(geometry) 

        distance_txt = "<h4> <b>Distance : " + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+ " Km </strong>" +"</h4></b>"
        duration_txt = "<h4> <b>Duration : " + "<strong>"+str(round(res['routes'][0]['summary']['duration']/60,1))+ " Min. </strong>" +"</h4></b>"

        folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt,max_width=300)).add_to(m)

        folium.Marker(
            location=list(coords[0][::-1]),
            popup="DEPART",
            icon=folium.Icon(color="green"),
            ).add_to(m)

        folium.Marker(
            location=list(coords[1][::-1]),
            popup="ARRIVEE",
            icon=folium.Icon(color="red"),
            ).add_to(m)

        return(m)

#interface 

#selection du tableau des noms des villes nous intéressant!

villes_interface = data_co.NOMGARE
for i in [5,17,18,32,34]:
    villes_interface = villes_interface.drop(i)
villes_interface = list(villes_interface)

def interface_carte(DEPART,ARRIVEE,k):
    '''fonction utilisée pour les widjets:interact, (DEPART/ARRIVEE : str, k:int)'''
    a = nb_sortie_possible(DEPART,ARRIVEE)
    if k > a:
        return('le nombre de sortie maximum est', a,'sortie(s)' )
    a = chemin_opt(DEPART,ARRIVEE,k)
    print('le trajet le moins cher pour', k)
    print('sortie est le trajet')
    print(a[0])
    print('il vous coûtera', a[1],'Euros')
    b = Graph()
    b = b.carte(DEPART,ARRIVEE)
    return(b)
