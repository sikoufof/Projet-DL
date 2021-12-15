#%%
from fonctions import *
#%%

# Connaître l'ensemble des sorties sur un trajet, (entré/sortie inclues)
chemint = chemin('VENDARGUES','SESQUIERES')
for i in range(len(chemint)):
    chemint[i] = re_transforme(chemint[i])
chemint


# Pour connaître le nombre de sortie intermédiare dans un trajet
nb_sortie_possible('VENDARGUES','BRAM')


# Pour connaître le coût direct d'un trajet 
cout_direct('VENDARGUES','BRAM')


# Pour connaître le meilleur trajet et le prix pour exactement 3 sorties
chemin_k_sortie('VENDARGUES','BRAM',3)
chemint = chemin_k_sortie('VENDARGUES','BRAM',3)
for i in range(len(chemint[0])):
    chemint[0][i] = re_transforme(chemint[0][i])
chemint


# Pour connaître le meilleur sortie et le prix en 5 sorties disponibles
chemin_opt('VENDARGUES','BRAM',5)


# Pour afficher un trajet sur une carte 
traj = Graph()
traj.carte('VENDARGUES','BRAM')


# Enfin pour avoir un interpréteur et manipuler facilement l'ensemble du code 
interact(interface_carte,DEPART=villes_interface,ARRIVEE=villes_interface,k=(0,25))
