**Documentation**
====================================

La démarche apportée est la suivante : 
On décide de partitionner les portions de en 5 parties 



Dans cette partie de documentation, nous allons présenter les parties principales du code utilisés, 
l'entiéreté du code est disponlible sur le lien GitHub, ces différentes parties vont permettre à la finalité 
d'obtenir ,par exemple, une représentation cartographiée d'un itinéiare ou encore de calculer l'itinéraire 
le moins coûteux pour les automobilistes

La liste des packages importé sont disponibles dans le code source du projet.

.. code-block:: python

    fonction chemin : 

    Arguments : (Entrée = str, Sortie = str)

    Renvoie : (List) Liste d entier 



La fonction chemin va permettre de lister l'ensemble des sorties intermédiaires (entrée/sortie inclus) d'un trajet 
.. code-block:: python

    Voici un exemple d'utilisation : chemin('VENDARGUES','BRAM') -> [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 20, 21, 22, 23]

Pour décoder les valeurs on peut utiliser la fonction 
    
.. code-block:: python

    transforme : (Entrée = int) -> str


.. code-block:: python
 fonction chemin_opt(Entrée = str, Sortie = str, nombre de sortie k = int) -> list 


cette fonction permet d'obtenir le trajet le moins cher sous la conditions de pouvoir 
effectuer k sortie entre temps, elle donne également le prix du trajet 

.. code-block:: python

    Voici un exemple d'utilisation chemin_opt('VENDARGUES','BRAM',3) -> [['VENDARGUES', 'AGDE', 'BEZIERS OUEST', 'LEZIGNAN', 'BRAM'], 13.5]

la suite des fonction disponibles vont permettre d'obtenir une représentation graphique du trajet 
et également une interface graphique.

la classe Graph va permettre de créer une carte géographique et également de tracer l'itinéraire 
entre une entré et une sortie, voici un exemple d'utilsation :

.. code-block:: python
    a = Graph()
    a.carte(Entré = str, Sortie = str) une clée API est déja fournie, toute fois, cette clée doit 
    être créer par ses soins.

    a.carte('VENDARGUES','BRAM')

Enfin on peut obtnir une interface graphique avec interact 

Voici un exemple d'utilisation : 

.. code-block:: python

 interact(interface_carte,DEPART=villes_interface,ARRIVEE=villes_interface,k=(0,25))

la fonction interface_carte(Entrée = str, Sortie = str, k = int) -> map 

permettant d'obtenir la carte graphique, le traket et le prix du chemin le moins couteux.


