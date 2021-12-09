**Documentation**
====================================

La démarche apportée est la suivante : 
On décide de partitionner les portions de en 5 parties 


**Importation des données**
--------------------------------

.. code-block:: python

    dta1 = pd.read_csv("gares-peage-2019.csv", sep = ';')
    dta1.rename({' NomGare ':'NomGare'},axis=1,inplace=True)
    data_co = pd.read_csv("coordonnees.csv", sep = ',')
    price = pd.read_csv("DataFrame_price.csv", sep=';')
    price = price.fillna(0)
    price.columns = ([0]+list(data_co.NOMGARE))
    price.index = list(data_co.NOMGARE)


