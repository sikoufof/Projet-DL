**Demarche**
==============

Il vous suffira de téléchager les données que nous avons utilisées pour la réalisation de ce projet.

Dans cette partie, vous aurez les codes python essentiels qui nous a permis de réaliser ce projet.


**Importation des données**
--------------------------------

.. code:: python

    dta1 = pd.read_csv("gares-peage-2019.csv", sep = ';')
    dta1.rename({' NomGare ':'NomGare'},axis=1,inplace=True)


    data_co = pd.read_csv("coordonnees.csv", sep = ',')

    price = pd.read_csv("DataFrame_price.csv", sep=';')
    price = price.fillna(0)

    price.columns = ([0]+list(data_co.NOMGARE))
    price.index = list(data_co.NOMGARE)


**Création du tableau des distances et Extraction des données relatives aux autoroutes** 
----------------------------------------------------------------------------------------------------------------------

Il doit y avoir une valeur x et y dans le csv sous forme de string:'2' à la place de seulement 2, ex dta1.loc[0,'x']='2'

.. code:: python

    for i in range(len(dta1.index)):
    dta1.loc[i,'x']=float(dta1.loc[i,'x'].replace(',','.'))
    dta1.loc[i,'y']=float(dta1.loc[i,'y'].replace(',','.'))

    dta_routes = dta1[(dta1.route=="A0009")|(dta1.route=="A0709")|(dta1.route=="A0061")|(dta1.route=="A0062")|(dta1.route=="A0075")|(dta1.route=="A0066")]  
    dta_routes = dta_routes[['route','NomGare','x','y']]


**Reaffectations des indices**
-------------------------------

.. code:: python

    dta_routes.reset_index(drop = True, inplace = True)
    dta_routes


**Transformation des coordonnées Lambert93 en coordonéees GPS**

.. code:: python

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

**Suppression des autoroutes non concernées**
-----------------------------------------------------------------

.. code:: python

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


    